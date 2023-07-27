use clap::Parser;
use indicatif::{MultiProgress, ProgressBar, ProgressStyle};
use itertools::{izip, Itertools};
use lazy_static::lazy_static;
use regex::Regex;
use std::{collections::HashMap, fs::File, io::Read};

const TASK: usize = 1;
const PID: usize = 2;
/// whole part of the timestamp in microseconds
const TS1: usize = 3;
/// decimal part of the timestamp in microseconds
const TS2: usize = 4;
/// type of the event. "B" corresponds to trace beginning and "E" to trace
/// ending. Due to how traces work, "E" does not have an associated name and
/// instead closes the last trace that was opened.
const TYPE: usize = 5;
/// PID of the traced process
const TPID: usize = 6;
/// name of the traced event
const NAME: usize = 7;

lazy_static! {
    // regex for lines in the trace file, the capture groups are described by
    // the previous constants
    static ref ROW_REGEX: Regex = Regex::new(r#"^\s*(.+?)\s+\(\s*([0-9\-]+)\s*\)\s*\[\d+\]\s*.{4}\s*(\d+)\.(\d+):\s+tracing_mark_write:\s+([EB])\|(\d+)\|?(.*)?$"#).unwrap();
}

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    #[clap(short, long)]
    dir: String,
    #[clap(short, long, default_value_t = 0)]
    start: usize,
    #[clap(short, long, default_value_t = 0)]
    end: usize,
    #[clap(short, long)]
    apps: String,
    #[clap(short, long, default_value = "out.csv")]
    out: String,
}

#[derive(Debug)]
struct RawTrace {
    start: f64,
    ts: f64,
    name: String,
}

struct Trace {
    name: String,
    server: f64,
    guest: f64,
    dynamic_proxy: f64,
    preload: f64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let apps = serde_yaml::from_reader(File::open(args.apps)?)?;
    let out_file = File::create(&args.out)?;
    let mut wrt = csv::Writer::from_writer(out_file);
    wrt.write_record(&["app", "server", "guest", "dynamic_proxy", "preload"])?;

    let traces = parse_all_traces(apps, &args.dir, args.start, args.end)?;

    for trace in traces {
        wrt.write_record(&[
            trace.name,
            trace.server.to_string(),
            trace.guest.to_string(),
            trace.dynamic_proxy.to_string(),
            trace.preload.to_string(),
        ])?;
    }
    wrt.flush()?;
    Ok(())
}

/// parse multiple trace files for multiple apps, collect the traces, and extract
/// the traces related to VirtualPatch events (load server patch, preload, etc.)
fn parse_all_traces(
    apps: Vec<String>,
    dir: &str,
    start: usize,
    mut end: usize,
) -> Result<Vec<Trace>, Box<dyn std::error::Error>> {
    let mut out = Vec::new();
    let mut parse_all = false;
    if start == 0 && end == 0 {
        end = 1000;
        parse_all = false;
    }

    let pb = ProgressBar::new(((end - start + 1) * apps.len()) as u64);
    let style = ProgressStyle::default_bar()
        .template("[{elapsed_precise}/{eta_precise}] {bar:40.cyan/blue} {pos:>7}/{len:7} {msg}")
        .progress_chars("##-");
    pb.set_style(style.clone());
    for i in start..end + 1 {
        for app in &apps {
            pb.inc(1);
            pb.set_message(format!("{} {}", app, i).as_str());
            let filename = format!("{}/{}-{}.htm", dir, app, i);
            // println!("parsing {}...", filename);
            match File::open(filename) {
                Ok(mut f) => {
                    let mut buf = String::new();
                    f.read_to_string(&mut buf)?;
                    match parse_traces(&buf) {
                        Some(raw) => {
                            let server: Vec<_> = raw
                                .iter()
                                .filter(|t| t.name == "ServerPatch")
                                .sorted_by(|a, b| a.ts.partial_cmp(&b.ts).unwrap())
                                .collect();
                            let guest: Vec<_> = raw
                                .iter()
                                .filter(|t| t.name == "GuestPatch")
                                .sorted_by(|a, b| a.ts.partial_cmp(&b.ts).unwrap())
                                .collect();
                            let dp: Vec<_> = raw
                                .iter()
                                .filter(|t| t.name == "DynamicProxyPatch")
                                .sorted_by(|a, b| a.ts.partial_cmp(&b.ts).unwrap())
                                .collect();
                            let preload: Vec<_> =
                                raw.iter().filter(|t| t.name == "preloadPatches").collect();
                            for (s, g, d, p) in
                                izip!(server.iter(), guest.iter(), dp.iter(), preload.iter())
                            {
                                out.push(Trace {
                                    name: app.to_string(),
                                    server: s.ts * 1000f64,
                                    guest: g.ts * 1000f64,
                                    dynamic_proxy: d.ts * 1000f64,
                                    preload: p.ts * 1000f64,
                                })
                            }
                        }
                        None => println!("no trace found for {} {}", app, i),
                    }
                }
                Err(e) => {
                    if parse_all {
                        break;
                    }
                    return Err(Box::new(e));
                }
            }
        }
    }
    pb.finish();
    Ok(out)
}

/// parses the traces in a file and returns a vector containing the raw traces.
/// The raw traces can then be filtered for specific events etc.
fn parse_traces(buf: &str) -> Option<Vec<RawTrace>> {
    let mut state = HashMap::<String, Vec<(String, f64)>>::new();
    let mut out = Vec::new();
    let start = buf.find("tracer: nop")?;
    let (_, trace_data) = buf.split_at(start);
    for t in trace_data.lines() {
        if let Some(res) = ROW_REGEX.captures(t) {
            let kind = res.get(TYPE).unwrap().as_str();
            let pid = res.get(TPID).unwrap().as_str();
            let ts1 = res.get(TS1).unwrap().as_str(); // microseconds
            let ts2 = res.get(TS2).unwrap().as_str(); // decimal microseconds
            let ts = format!("{}.{}", ts1, ts2);
            let ts: f64 = ts.parse().ok()?;
            if kind == "B" {
                // begin of a trace, this has a name, "opens" the trace
                let name = res.get(NAME).unwrap().as_str().to_owned();
                let data = (name, ts);
                if !state.contains_key(pid) {
                    state.insert(pid.into(), Vec::new());
                }
                state.get_mut(pid).unwrap().push(data);
            } else if kind == "E" && state.contains_key(pid) && state[pid].len() > 0 {
                // this is the end of a trace, however it does not have a name
                // but it "closes" the last opened trace
                let last = state.get_mut(pid).unwrap().pop().unwrap();
                let diff = ts - last.1;
                out.push(RawTrace {
                    start: last.1,
                    ts: diff,
                    name: last.0,
                });
            }
        }
    }
    Some(out)
}
