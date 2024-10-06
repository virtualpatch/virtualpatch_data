package dev.virtualpatch.patch;

public class NativeLoader {
    public static void loadPatch(String lib) {
        System.load(lib);
        nativeLoad();
    }
    private static native void nativeLoad();
}