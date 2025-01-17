package io.virtualapp.home;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.os.Bundle;
import androidx.annotation.Nullable;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.lody.virtual.client.core.VirtualCore;
import com.lody.virtual.client.ipc.VPackageManager;
import com.xdja.zs.DataCleanManager;

import io.virtualapp.R;
import io.virtualapp.abs.ui.VActivity;
import io.virtualapp.home.models.PackageAppData;
import io.virtualapp.home.repo.PackageAppDataStorage;

/**
 * @author Lody
 */
public class AppSettingActivity extends VActivity {

    private PackageAppData mData;
    private int mUserId;
    private PackageInfo mPkgInfo;

    public static void enterAppSetting(Context context, String pkg, int userId) {
        Intent intent = new Intent(context, AppSettingActivity.class);
        intent.putExtra("extra.PKG", pkg);
        intent.putExtra("extra.UserId", userId);
        context.startActivity(intent);
    }

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Intent intent = getIntent();
        String pkg = intent.getStringExtra("extra.PKG");
        mUserId = intent.getIntExtra("extra.UserId", -1);
        mData = PackageAppDataStorage.get().acquire(pkg);
        mPkgInfo = VPackageManager.get().getPackageInfo(pkg, 0, mUserId);
        if (mData == null || mPkgInfo == null) {
            finish();
            return;
        }
        enableBackHome();
        setTitle(R.string.app_settings);
        setContentView(R.layout.activity_app_setting);
        ImageView iconView = (ImageView) findViewById(R.id.app_icon);
        TextView nameView = (TextView) findViewById(R.id.app_name);
        TextView labelView = (TextView) findViewById(R.id.app_label);

        labelView.setText(getString(R.string.label_app_data_szie, DataCleanManager.getPackageFolderSize(0, pkg, DataCleanManager.FOLDER_TYPE_DATA)));
        iconView.setImageDrawable(mData.icon);
        nameView.setText(mData.name);
        findViewById(R.id.btn_clean_data).setOnClickListener(v -> {
            cleanAppData();
            labelView.setText(getString(R.string.label_app_data_szie, DataCleanManager.getPackageFolderSize(0, pkg, DataCleanManager.FOLDER_TYPE_DATA)));
        });
    }

    private void cleanAppData() {
        boolean res = VirtualCore.get().cleanPackageData(mPkgInfo.packageName, mUserId);
        Toast.makeText(this, "clean app data " + (res ? "success." : "failed."), Toast.LENGTH_SHORT).show();

    }
}
