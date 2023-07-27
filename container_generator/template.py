GRADLE_SETTINGS = """
//include ':lib', ':app'
//, ':libsandhook'
include ':containerlib', ':container'
"""

GRADLE_SCRIPT = """
plugins {{
    id 'com.android.application'
}}

android {{
    namespace 'dev.sime1.container'
    compileSdkVersion 32

    defaultConfig {{
        applicationId "dev.sime1.container.{guest_package}"
        minSdkVersion 21
        buildConfigField 'String', 'GUEST_ID', '"{guest_package}"'
        targetSdkVersion 26
        versionCode 180080814
        versionName "2.2.3"
        multiDexEnabled false
        vectorDrawables.useSupportLibrary = true
        buildConfigField 'String', 'PACKAGE_NAME_ARM64', '"' + rootProject.ext.PACKAGE_NAME_ARM64 + '"'
        manifestPlaceholders = [
                PACKAGE_NAME_32BIT: rootProject.ext.PACKAGE_NAME_32BIT,
                PACKAGE_NAME_ARM64: rootProject.ext.PACKAGE_NAME_ARM64,
                APP_LABEL: "{guest_package} - Container"
        ]
        ndk {{
            abiFilters "arm64-v8a"//"armeabi-v7a"//,
        }}
    }}
    sourceSets {{
        main {{
            jniLibs.srcDirs = ['libs']
        }}
    }}

    buildTypes {{
        debug {{
            debuggable true
            jniDebuggable false
            minifyEnabled false
            //proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro', 'virtualapp-proguard-rules.pro'
        }}
        release {{
            minifyEnabled false
            //proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro', 'virtualapp-proguard-rules.pro'
        }}
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}

    lintOptions {{
        checkReleaseBuilds false
        // Or, if you prefer, you can continue to check for errors in release builds,
        // but continue the build even when errors are found:
        abortOnError false
    }}
    packagingOptions {{
        pickFirst '**/libbytehook.so'
    }}
}}


dependencies {{
    implementation fileTree(include: ['*.jar'], dir: '../app/libs')
    implementation project(':containerlib')
    implementation 'com.swift.sandhook:hooklib:4.2.0'
    implementation 'com.swift.sandhook:nativehook:4.2.0'
    implementation 'com.swift.sandhook:xposedcompat:4.2.0'
    //Android Lib
    implementation 'androidx.multidex:multidex:2.0.0'
    implementation 'androidx.percentlayout:percentlayout:1.0.0'
    implementation 'androidx.appcompat:appcompat:1.0.0'
    implementation 'androidx.recyclerview:recyclerview:1.0.0'
    implementation 'com.google.android.material:material:1.0.0'
    implementation 'androidx.cardview:cardview:1.0.0'
    //Lifecycles, LiveData, and ViewModel
    implementation 'androidx.lifecycle:lifecycle-runtime:2.0.0'
    implementation 'androidx.lifecycle:lifecycle-extensions:2.0.0'
    annotationProcessor 'androidx.lifecycle:lifecycle-compiler:2.0.0'
    //Room
    implementation 'androidx.room:room-runtime:2.0.0'
    annotationProcessor 'androidx.room:room-compiler:2.0.0'
    //Promise Support
    implementation 'org.jdeferred:jdeferred-android-aar:1.2.4'
    // ThirdParty
    implementation 'com.jonathanfinerty.once:once:1.0.3'
    //implementation 'com.xdja.safekeyservice:xdjacrypto:1.0.3'
    //implementation 'com.xdja.safekeyservice:jar_multi_jniapi:3.9.50'
    //implementation 'com.xdja.safekeyservice:jar_multi_unitepin:3.9.24'
    implementation files('../app/libs/securitysdk-v2--standard-4.0.12.2477.jar')
    implementation 'com.google.code.gson:gson:2.6.2'
}}
"""

MANIFEST = """<?xml version="1.0"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="com.lody.virtual">

    <permission
        android:name="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
        android:protectionLevel="signature" />

    <application
        android:vmSafeMode="true">

        <service
            android:name="com.lody.virtual.client.stub.KeepAliveService"
            android:process="@string/engine_process_name" />

        <service
            android:name="com.lody.virtual.client.stub.HiddenForeNotification"
            android:process="@string/engine_process_name" />

        <activity
            android:excludeFromRecents="true"
            android:name="com.lody.virtual.client.stub.ShortcutHandleActivity"
            android:exported="true"
            android:process="@string/engine_process_name"
            android:taskAffinity="virtual.shortcut.task"
            android:theme="@android:style/Theme.Translucent.NoTitleBar">
            <intent-filter>
                <action android:name="${applicationId}.virtual.action.shortcut" />

                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
            </intent-filter>
        </activity>

        <activity
            android:theme="@android:style/Theme.Translucent.NoTitleBar"
            android:name=".client.stub.ShadowPendingActivity"
            android:excludeFromRecents="true"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name"
            android:taskAffinity="com.lody.virtual.pending" />

        <service
            android:name=".client.stub.ShadowPendingService"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name" />
        <receiver
            android:name=".client.stub.ShadowPendingReceiver"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name" />

        <service
            android:name=".client.stub.ShadowJobService"
            android:exported="true"
            android:permission="android.permission.BIND_JOB_SERVICE"
            android:process="@string/engine_process_name" />

        <service
            android:name=".client.stub.ShadowJobWorkService"
            android:process="@string/engine_process_name" />

        <activity
            android:name=".client.stub.ChooseAccountTypeActivity"
            android:configChanges="keyboard|keyboardHidden|orientation"
            android:excludeFromRecents="true"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name" />

        <activity
            android:name=".client.stub.ChooseTypeAndAccountActivity"
            android:configChanges="keyboard|keyboardHidden|orientation"
            android:excludeFromRecents="true"
            android:exported="false"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name" />

        <activity
            android:name=".client.stub.ShadowNfcDispatcher"
            android:configChanges="keyboard|keyboardHidden|orientation"
            android:excludeFromRecents="true"
            android:theme="@android:style/Theme.Translucent.NoTitleBar"
            android:taskAffinity="com.lody.virtual.choose"
            android:process="@string/engine_process_name"
            android:exported="true">
            <intent-filter>
                <action android:name="android.nfc.action.TECH_DISCOVERED"/>
                <category android:name="android.intent.category.DEFAULT"/>
            </intent-filter>
            <meta-data android:name="android.nfc.action.TECH_DISCOVERED" android:resource="@xml/nfc_tech_filter"/>
        </activity>

        <activity
            android:name=".client.stub.TechListChooserActivity"
            android:configChanges="keyboard|keyboardHidden|orientation"
            android:excludeFromRecents="true"
            android:exported="true"
            android:finishOnCloseSystemDialogs="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name"
            android:taskAffinity="com.lody.virtual.choose"
            android:theme="@style/VAAlertTheme" />

        <activity
            android:name=".client.stub.ChooserActivity"
            android:configChanges="keyboard|keyboardHidden|orientation"
            android:excludeFromRecents="true"
            android:exported="true"
            android:finishOnCloseSystemDialogs="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name"
            android:taskAffinity="com.lody.virtual.choose"
            android:theme="@style/VAAlertTheme" />

        <activity
            android:name=".client.stub.ResolverActivity"
            android:configChanges="keyboard|keyboardHidden|orientation"
            android:excludeFromRecents="true"
            android:exported="true"
            android:finishOnCloseSystemDialogs="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name"
            android:taskAffinity="com.lody.virtual.choose"
            android:theme="@style/VAAlertTheme" />

        <!--xdja-->
        <activity android:name=".client.stub.InstallerActivity"
            android:configChanges="keyboard|keyboardHidden|orientation"
            android:excludeFromRecents="true"
            android:exported="true"
            android:finishOnCloseSystemDialogs="true"
            android:process="@string/engine_process_name"
            android:taskAffinity="com.xdja.safety.Installer"
            android:theme="@style/InstallerTheme" >
            <intent-filter>
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </activity>
        <activity android:name=".client.stub.UnInstallerActivity"
            android:configChanges="keyboard|keyboardHidden|orientation"
            android:excludeFromRecents="true"
            android:exported="true"
            android:finishOnCloseSystemDialogs="true"
            android:process="@string/engine_process_name"
            android:taskAffinity="com.xdja.safety.Installer"
            android:theme="@style/InstallerTheme" >
            <intent-filter>
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </activity>
        <!--xdja-->

        <provider
            android:name="com.lody.virtual.server.BinderProvider"
            android:authorities="${AUTHORITY_PREFIX}.virtual.service.BinderProvider"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P0"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p0"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P1"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p1"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P2"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p2"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P3"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p3"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P4"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p4"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P5"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p5"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P6"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p6"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P7"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p7"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P8"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p8"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P9"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p9"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P10"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p10"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P11"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p11"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P12"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p12"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P13"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p13"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P14"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p14"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P15"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p15"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P16"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p16"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P17"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p17"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P18"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p18"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P19"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p19"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P20"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p20"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P21"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p21"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P22"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p22"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P23"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p23"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P24"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p24"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P25"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p25"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P26"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p26"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P27"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p27"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P28"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p28"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P29"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p29"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P30"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p30"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P31"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p31"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P32"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p32"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P33"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p33"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P34"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p34"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P35"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p35"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P36"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p36"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P37"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p37"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P38"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p38"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P39"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p39"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P40"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p40"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P41"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p41"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P42"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p42"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P43"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p43"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P44"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p44"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P45"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p45"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P46"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p46"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P47"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p47"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P48"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p48"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P49"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p49"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P50"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p50"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P51"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p51"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P52"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p52"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P53"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p53"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P54"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p54"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P55"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p55"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P56"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p56"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P57"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p57"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P58"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p58"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P59"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p59"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P60"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p60"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P61"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p61"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P62"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p62"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P63"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p63"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P64"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p64"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P65"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p65"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P66"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p66"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P67"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p67"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P68"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p68"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P69"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p69"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P70"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p70"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P71"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p71"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P72"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p72"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P73"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p73"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P74"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p74"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P75"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p75"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P76"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p76"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P77"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p77"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P78"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p78"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P79"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p79"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P80"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p80"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P81"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p81"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P82"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p82"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P83"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p83"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P84"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p84"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P85"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p85"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P86"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p86"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P87"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p87"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P88"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p88"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P89"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p89"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P90"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p90"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P91"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p91"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P92"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p92"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P93"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p93"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P94"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p94"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P95"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p95"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P96"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p96"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P97"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p97"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P98"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p98"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowActivity$P99"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p99"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@style/VATheme" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P0"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p0"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P1"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p1"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P2"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p2"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P3"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p3"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P4"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p4"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P5"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p5"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P6"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p6"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P7"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p7"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P8"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p8"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P9"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p9"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P10"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p10"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P11"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p11"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P12"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p12"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P13"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p13"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P14"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p14"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P15"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p15"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P16"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p16"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P17"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p17"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P18"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p18"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P19"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p19"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P20"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p20"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P21"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p21"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P22"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p22"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P23"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p23"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P24"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p24"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P25"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p25"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P26"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p26"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P27"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p27"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P28"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p28"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P29"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p29"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P30"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p30"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P31"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p31"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P32"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p32"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P33"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p33"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P34"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p34"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P35"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p35"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P36"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p36"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P37"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p37"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P38"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p38"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P39"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p39"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P40"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p40"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P41"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p41"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P42"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p42"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P43"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p43"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P44"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p44"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P45"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p45"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P46"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p46"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P47"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p47"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P48"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p48"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P49"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p49"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P50"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p50"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P51"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p51"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P52"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p52"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P53"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p53"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P54"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p54"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P55"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p55"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P56"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p56"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P57"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p57"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P58"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p58"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P59"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p59"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P60"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p60"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P61"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p61"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P62"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p62"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P63"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p63"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P64"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p64"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P65"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p65"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P66"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p66"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P67"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p67"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P68"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p68"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P69"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p69"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P70"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p70"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P71"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p71"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P72"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p72"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P73"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p73"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P74"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p74"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P75"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p75"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P76"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p76"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P77"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p77"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P78"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p78"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P79"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p79"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P80"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p80"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P81"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p81"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P82"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p82"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P83"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p83"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P84"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p84"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P85"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p85"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P86"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p86"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P87"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p87"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P88"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p88"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P89"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p89"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P90"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p90"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P91"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p91"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P92"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p92"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P93"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p93"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P94"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p94"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P95"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p95"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P96"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p96"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P97"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p97"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P98"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p98"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <activity
            android:name="com.lody.virtual.client.stub.ShadowDialogActivity$P99"
            android:configChanges="mcc|mnc|locale|touchscreen|keyboard|keyboardHidden|navigation|orientation|screenLayout|uiMode|screenSize|smallestScreenSize|fontScale"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p99"
            android:taskAffinity="com.lody.virtual.virtual_task"
            android:theme="@android:style/Theme.Dialog" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P0"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p0" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P1"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p1" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P2"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p2" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P3"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p3" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P4"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p4" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P5"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p5" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P6"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p6" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P7"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p7" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P8"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p8" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P9"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p9" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P10"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p10" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P11"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p11" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P12"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p12" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P13"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p13" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P14"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p14" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P15"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p15" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P16"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p16" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P17"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p17" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P18"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p18" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P19"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p19" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P20"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p20" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P21"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p21" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P22"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p22" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P23"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p23" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P24"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p24" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P25"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p25" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P26"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p26" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P27"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p27" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P28"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p28" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P29"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p29" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P30"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p30" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P31"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p31" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P32"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p32" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P33"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p33" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P34"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p34" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P35"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p35" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P36"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p36" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P37"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p37" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P38"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p38" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P39"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p39" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P40"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p40" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P41"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p41" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P42"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p42" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P43"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p43" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P44"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p44" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P45"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p45" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P46"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p46" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P47"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p47" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P48"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p48" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P49"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p49" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P50"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p50" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P51"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p51" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P52"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p52" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P53"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p53" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P54"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p54" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P55"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p55" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P56"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p56" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P57"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p57" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P58"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p58" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P59"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p59" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P60"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p60" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P61"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p61" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P62"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p62" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P63"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p63" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P64"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p64" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P65"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p65" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P66"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p66" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P67"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p67" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P68"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p68" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P69"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p69" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P70"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p70" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P71"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p71" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P72"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p72" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P73"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p73" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P74"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p74" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P75"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p75" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P76"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p76" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P77"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p77" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P78"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p78" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P79"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p79" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P80"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p80" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P81"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p81" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P82"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p82" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P83"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p83" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P84"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p84" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P85"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p85" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P86"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p86" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P87"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p87" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P88"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p88" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P89"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p89" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P90"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p90" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P91"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p91" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P92"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p92" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P93"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p93" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P94"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p94" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P95"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p95" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P96"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p96" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P97"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p97" />

        <service
            android:name="com.lody.virtual.client.stub.ShadowService$P98"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p98" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P0"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_0"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p0" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P1"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_1"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p1" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P2"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_2"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p2" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P3"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_3"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p3" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P4"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_4"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p4" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P5"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_5"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p5" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P6"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_6"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p6" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P7"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_7"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p7" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P8"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_8"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p8" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P9"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_9"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p9" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P10"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_10"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p10" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P11"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_11"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p11" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P12"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_12"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p12" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P13"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_13"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p13" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P14"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_14"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p14" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P15"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_15"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p15" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P16"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_16"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p16" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P17"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_17"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p17" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P18"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_18"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p18" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P19"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_19"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p19" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P20"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_20"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p20" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P21"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_21"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p21" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P22"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_22"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p22" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P23"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_23"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p23" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P24"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_24"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p24" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P25"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_25"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p25" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P26"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_26"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p26" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P27"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_27"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p27" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P28"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_28"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p28" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P29"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_29"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p29" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P30"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_30"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p30" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P31"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_31"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p31" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P32"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_32"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p32" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P33"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_33"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p33" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P34"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_34"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p34" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P35"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_35"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p35" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P36"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_36"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p36" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P37"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_37"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p37" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P38"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_38"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p38" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P39"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_39"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p39" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P40"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_40"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p40" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P41"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_41"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p41" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P42"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_42"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p42" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P43"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_43"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p43" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P44"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_44"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p44" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P45"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_45"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p45" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P46"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_46"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p46" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P47"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_47"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p47" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P48"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_48"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p48" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P49"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_49"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p49" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P50"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_50"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p50" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P51"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_51"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p51" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P52"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_52"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p52" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P53"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_53"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p53" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P54"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_54"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p54" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P55"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_55"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p55" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P56"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_56"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p56" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P57"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_57"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p57" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P58"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_58"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p58" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P59"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_59"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p59" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P60"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_60"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p60" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P61"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_61"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p61" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P62"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_62"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p62" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P63"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_63"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p63" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P64"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_64"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p64" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P65"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_65"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p65" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P66"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_66"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p66" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P67"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_67"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p67" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P68"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_68"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p68" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P69"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_69"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p69" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P70"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_70"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p70" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P71"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_71"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p71" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P72"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_72"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p72" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P73"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_73"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p73" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P74"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_74"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p74" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P75"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_75"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p75" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P76"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_76"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p76" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P77"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_77"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p77" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P78"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_78"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p78" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P79"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_79"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p79" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P80"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_80"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p80" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P81"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_81"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p81" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P82"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_82"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p82" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P83"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_83"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p83" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P84"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_84"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p84" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P85"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_85"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p85" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P86"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_86"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p86" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P87"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_87"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p87" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P88"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_88"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p88" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P89"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_89"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p89" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P90"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_90"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p90" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P91"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_91"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p91" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P92"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_92"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p92" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P93"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_93"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p93" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P94"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_94"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p94" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P95"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_95"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p95" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P96"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_96"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p96" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P97"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_97"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p97" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P98"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_98"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p98" />

        <provider
            android:name="com.lody.virtual.client.stub.ShadowContentProvider$P99"
            android:authorities="${AUTHORITY_PREFIX}.virtual_stub_99"
            android:exported="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process=":p99" />

        <!-- 放在main进程，用来读取外部的provider -->
        <provider
            android:name=".client.stub.OutsideProxyContentProvider"
            android:authorities="${AUTHORITY_PREFIX}.provider_outside"
            android:exported="false" />

        <provider
            android:name=".client.stub.ContentProviderProxy"
            android:authorities="${AUTHORITY_PREFIX}.provider_proxy"
            android:exported="true"
            android:grantUriPermissions="true"
            android:process=":x" />

        <provider
            android:name="com.xdja.ckms.TokenProvider"
            android:authorities="${AUTHORITY_PREFIX}.TokenProvider"
            android:enabled="true"
            android:exported="true">
        </provider>

        <activity
            android:name=".client.stub.WindowPreviewActivity"
            android:excludeFromRecents="true"
            android:launchMode="singleTop"
            android:process=":x"
            android:taskAffinity="com.lody.virtual.window_preview"
            android:theme="@style/WindowBackgroundTheme" />

        <activity
            android:name=".client.stub.RequestPermissionsActivity"
            android:excludeFromRecents="true"
            android:exported="true"
            android:launchMode="singleInstance"
            android:taskAffinity="com.lody.virtual.request_permission"
            android:theme="@android:style/Theme.Translucent.NoTitleBar" />

        <service
            android:name="com.xdja.call.PhoneCallService"
            android:process=":x"
            android:permission="android.permission.BIND_INCALL_SERVICE">
            <meta-data
                android:name="android.telecom.IN_CALL_SERVICE_UI"
                android:value="true" />
            <intent-filter>
                <action android:name="android.telecom.InCallService" />
            </intent-filter>
        </service>

        <service
            android:name="com.xdja.zs.NotificationListener"
            android:permission="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE">
            <intent-filter>
                <action android:name="android.service.notification.NotificationListenerService"/>
            </intent-filter>
        </service>

        <activity android:name="com.xdja.call.DialerActivity">
            <intent-filter>
                <action android:name="android.intent.action.DIAL" />
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="tel" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.DIAL" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </activity>
        <receiver
            android:name="com.xdja.call.PhoneCallReceiver"
            android:enabled="true"
            android:exported="true">
        </receiver>


        <!-- Intents for KLP+ Delivery -->
        <receiver android:name="com.xdja.mms.receiver.MmsWapPushDeliverReceiver"
            android:process=":x"
            android:permission="android.permission.BROADCAST_WAP_PUSH">
            <intent-filter>
                <action android:name="android.provider.Telephony.WAP_PUSH_DELIVER" />
                <data android:mimeType="application/vnd.wap.mms-message" />
            </intent-filter>
        </receiver>
        <receiver android:name="com.xdja.mms.receiver.SmsDeliverReceiver"
            android:process=":x"
            android:permission="android.permission.BROADCAST_SMS">
            <intent-filter>
                <action android:name="android.provider.Telephony.SMS_DELIVER" />
            </intent-filter>
        </receiver>
        <receiver android:name="com.xdja.mms.receiver.SmsReceiver"
            android:permission="android.permission.BROADCAST_SMS"
            android:process=":x">
            <intent-filter android:priority="2147483647">
                <action android:name="android.provider.Telephony.SMS_RECEIVED"/>
            </intent-filter>
            <intent-filter android:priority="2147483647">
                <action android:name="android.provider.Telephony.MMS_DOWNLOADED"/>
            </intent-filter>
        </receiver>

        <!-- Activity that allows the user to send new SMS/MMS messages -->
        <activity
            android:name="com.xdja.mms.LaunchConversationActivity"
            android:configChanges="orientation|screenSize|keyboardHidden"
            android:process=":x"
            android:screenOrientation="user"
            android:excludeFromRecents="true"
            android:theme="@android:style/Theme.Translucent.NoTitleBar">
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <action android:name="android.intent.action.SENDTO" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="sms" />
                <data android:scheme="smsto" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <action android:name="android.intent.action.SENDTO" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="mms" />
                <data android:scheme="mmsto" />
            </intent-filter>
        </activity>

        <service android:name="com.xdja.mms.NoConfirmationSmsSendService"
            android:process=":x"
            android:permission="android.permission.SEND_RESPOND_VIA_MESSAGE"
            android:exported="true" >
            <intent-filter>
                <action android:name="android.intent.action.RESPOND_VIA_MESSAGE" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:scheme="sms" />
                <data android:scheme="smsto" />
                <data android:scheme="mms" />
                <data android:scheme="mmsto" />
            </intent-filter>
        </service>

        <activity
            android:name="com.xdja.zs.UacProxyActivity"
            android:configChanges="orientation|keyboardHidden|screenSize"
            android:theme="@android:style/Theme.Translucent.NoTitleBar.Fullscreen">
            <intent-filter>
                <data android:scheme="xdja" android:host="${AUTHORITY_PREFIX}" android:path="/authorize"/>
                <category android:name="android.intent.category.DEFAULT"/>
                <action android:name="android.intent.action.VIEW"/>
                <category android:name="android.intent.category.BROWSABLE"/>
            </intent-filter>
        </activity>

        <activity
            android:name="com.lody.virtual.client.stub.usb.ShadowUsbActivity"
            android:configChanges="locale|keyboardHidden|orientation|screenSize|fontScale"
            android:excludeFromRecents="true"
            android:theme="@android:style/Theme.Translucent.NoTitleBar"
            android:taskAffinity="com.lody.virtual.choose"
            android:launchMode="singleTop">
            <intent-filter>
                <action android:name="android.hardware.usb.action.USB_DEVICE_ATTACHED" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.hardware.usb.action.USB_DEVICE_DETACHED" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
            </intent-filter>
            <meta-data
                android:name="android.hardware.usb.action.USB_DEVICE_ATTACHED"
                android:resource="@xml/usb_llvision_device_filter" />
        </activity>
        <activity
            android:name=".client.stub.usb.UsbListChooserActivity"
            android:configChanges="keyboard|keyboardHidden|orientation"
            android:excludeFromRecents="true"
            android:exported="true"
            android:finishOnCloseSystemDialogs="true"
            android:permission="${PERMISSION_PREFIX}.permission.SAFE_ACCESS"
            android:process="@string/engine_process_name"
            android:taskAffinity="com.lody.virtual.choose"
            android:theme="@style/VAAlertTheme" />

        <meta-data android:name="android.vivo_nightmode_support" android:value="false"/>
        <meta-data android:name="com.coloros.DisableSystemDarkMode" android:value="true"/>

        <!-- sms -->
        <meta-data
            android:name="VA_VERSION"
            android:value="${VA_VERSION}" />
        <!--<meta-data
            android:name="android.notch_support"
            android:value="true" />-->
    </application>
</manifest>
"""