# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import tempfile
import time
from PIL import Image

PROJECT_DIR = r"c:\Users\User\OneDrive\Desktop\MY IA FOR ARTIFICIAL INTELLIGENCE\Philip_Face_Recognition_Project"
BUILD_DIR = os.path.join(tempfile.gettempdir(), f"face_ai_build_{int(time.time())}")
OUTPUT_APK = os.path.join(PROJECT_DIR, "Philip_Face_AI.apk")

JAVA_HOME = r"C:\Program Files\Android\Android Studio\jbr"
JAVA_BIN = os.path.join(JAVA_HOME, "bin")
BUILD_TOOLS = r"C:\Users\User\AppData\Local\Android\Sdk\build-tools\36.1.0"
ANDROID_JAR = r"C:\Users\User\AppData\Local\Android\Sdk\platforms\android-36.1\android.jar"

os.environ["JAVA_HOME"] = JAVA_HOME
os.environ["PATH"] = JAVA_BIN + os.pathsep + BUILD_TOOLS + os.pathsep + os.environ["PATH"]

AAPT2 = os.path.join(BUILD_TOOLS, "aapt2.exe")
D8_JAR = os.path.join(BUILD_TOOLS, "lib", "d8.jar")
APKSIGNER_JAR = os.path.join(BUILD_TOOLS, "lib", "apksigner.jar")
ZIPALIGN = os.path.join(BUILD_TOOLS, "zipalign.exe")
JAVA_EXE = os.path.join(JAVA_BIN, "java.exe")
JAVAC = os.path.join(JAVA_BIN, "javac.exe")
KEYTOOL = os.path.join(JAVA_BIN, "keytool.exe")

print("1. Preparing build directories...")
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
os.makedirs(BUILD_DIR, exist_ok=True)

SRC_DIR = os.path.join(BUILD_DIR, "src", "org", "pentecost", "philip", "faceai")
RES_DIR = os.path.join(BUILD_DIR, "res")
ASSETS_DIR = os.path.join(BUILD_DIR, "assets")
BIN_DIR = os.path.join(BUILD_DIR, "bin")
COMPILED_RES = os.path.join(BUILD_DIR, "compiled_res")

os.makedirs(SRC_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(BIN_DIR, exist_ok=True)
os.makedirs(COMPILED_RES, exist_ok=True)

# 2. Icon setup
MIPMAP_DIR = os.path.join(RES_DIR, "mipmap")
os.makedirs(MIPMAP_DIR, exist_ok=True)
icon_path = os.path.join(PROJECT_DIR, "ic_launcher.png")
if os.path.exists(icon_path):
    shutil.copyfile(icon_path, os.path.join(MIPMAP_DIR, "ic_launcher.png"))
    print("✔ Loaded app icon into res/mipmap/ic_launcher.png")

# 3. Copy Web Assets to APK Assets
shutil.copyfile(os.path.join(PROJECT_DIR, "index.html"), os.path.join(ASSETS_DIR, "index.html"))

# Copy sample figures if present
figures_dir = os.path.join(PROJECT_DIR, "figures")
assets_fig = os.path.join(ASSETS_DIR, "figures")
if os.path.exists(figures_dir):
    os.makedirs(assets_fig, exist_ok=True)
    for f in os.listdir(figures_dir):
        if f.lower().endswith((".jpg", ".png", ".jpeg")):
            shutil.copyfile(os.path.join(figures_dir, f), os.path.join(assets_fig, f))

print("✔ Copied web application and figures into APK assets/")

# 4. AndroidManifest.xml with camera permissions
manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.pentecost.philip.faceai"
    android:versionCode="2"
    android:versionName="1.1">

    <!-- Explicit SDK Targeting for 100% Samsung Galaxy & Android 14+ Compatibility -->
    <uses-sdk
        android:minSdkVersion="21"
        android:targetSdkVersion="34" />

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />

    <!-- Make hardware features optional so all budget & flagship devices install smoothly -->
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.camera.autofocus" android:required="false" />
    <uses-feature android:name="android.hardware.camera.front" android:required="false" />

    <!-- Universal Screen & Density Support for Samsung Galaxy A-series -->
    <supports-screens
        android:smallScreens="true"
        android:normalScreens="true"
        android:largeScreens="true"
        android:xlargeScreens="true"
        android:anyDensity="true" />

    <application
        android:label="Philip Face AI"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher"
        android:theme="@android:style/Theme.NoTitleBar"
        android:usesCleartextTraffic="true"
        android:hardwareAccelerated="true">

        <activity
            android:name="org.pentecost.philip.faceai.MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""
manifest_path = os.path.join(BUILD_DIR, "AndroidManifest.xml")
with open(manifest_path, "w", encoding="utf-8") as f:
    f.write(manifest_content)

# 5. MainActivity.java with Camera & Audio permissions in WebView
java_content = """package org.pentecost.philip.faceai;

import android.app.Activity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.content.pm.PackageManager;
import android.Manifest;

public class MainActivity extends Activity {
    private WebView webView;
    private static final int PERMISSION_REQ_CODE = 2026;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Request runtime Camera & Audio permissions if needed
        if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{
                Manifest.permission.CAMERA,
                Manifest.permission.RECORD_AUDIO
            }, PERMISSION_REQ_CODE);
        }

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(false);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                // Grant camera & audio permissions automatically to the webview
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        request.grant(request.getResources());
                    }
                });
            }
        });

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });

        // Load bundled cybernetic face AI application
        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }
}
"""
with open(os.path.join(SRC_DIR, "MainActivity.java"), "w", encoding="utf-8") as f:
    f.write(java_content)

# 6. Strings.xml
VALUES_DIR = os.path.join(RES_DIR, "values")
os.makedirs(VALUES_DIR, exist_ok=True)
with open(os.path.join(VALUES_DIR, "strings.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?><resources><string name="app_name">Philip Face AI</string></resources>')

print("✔ Manifest, Java source, and resources generated.")

# Step A: aapt2 compile
print("2. Compiling Android resources with aapt2...")
cmd_aapt_compile = f'"{AAPT2}" compile --dir "{RES_DIR}" -o "{COMPILED_RES}"'
res = subprocess.run(cmd_aapt_compile, shell=True, capture_output=True, text=True)
if res.returncode != 0:
    print("AAPT2 Compile Error:", res.stderr)
    exit(1)

# Step B: aapt2 link
print("3. Linking resources and generating APK skeleton...")
flats = [os.path.join(COMPILED_RES, f) for f in os.listdir(COMPILED_RES) if f.endswith(".flat")]
flats_args = " ".join([f'"{f}"' for f in flats])

UNALIGNED_APK = os.path.join(BUILD_DIR, "unaligned.apk")
cmd_aapt_link = (
    f'"{AAPT2}" link -I "{ANDROID_JAR}" '
    f'--manifest "{manifest_path}" '
    f'-A "{ASSETS_DIR}" '
    f'-o "{UNALIGNED_APK}" '
    f'--java "{BUILD_DIR}/src" '
    f'{flats_args} --auto-add-overlay'
)
res = subprocess.run(cmd_aapt_link, shell=True, capture_output=True, text=True)
if res.returncode != 0:
    print("AAPT2 Link Error:", res.stderr)
    exit(1)

# Step C: javac compile
print("4. Compiling Java source files with javac...")
java_files = []
for root, _, files in os.walk(os.path.join(BUILD_DIR, "src")):
    for f in files:
        if f.endswith(".java"):
            java_files.append(os.path.join(root, f))

cmd_javac = f'"{JAVAC}" -cp "{ANDROID_JAR}" -d "{BIN_DIR}" ' + " ".join([f'"{jf}"' for jf in java_files])
res = subprocess.run(cmd_javac, shell=True, capture_output=True, text=True)
if res.returncode != 0:
    print("Javac Error:", res.stderr)
    exit(1)

# Step D: d8 dex
print("5. Converting Java bytecode to Dalvik Executable (classes.dex) with d8...")
class_files = []
for root, _, files in os.walk(BIN_DIR):
    for f in files:
        if f.endswith(".class"):
            class_files.append(os.path.join(root, f))

cmd_d8 = f'"{JAVA_EXE}" -cp "{D8_JAR}" com.android.tools.r8.D8 --min-api 21 --output "{BUILD_DIR}" --lib "{ANDROID_JAR}" ' + " ".join([f'"{cf}"' for cf in class_files])
res = subprocess.run(cmd_d8, shell=True, capture_output=True, text=True)
if res.returncode != 0:
    print("D8 Error:", res.stderr)
    exit(1)

# Step E: Add classes.dex to APK
print("6. Packaging classes.dex into APK...")
import zipfile
with zipfile.ZipFile(UNALIGNED_APK, "a") as zip_apk:
    zip_apk.write(os.path.join(BUILD_DIR, "classes.dex"), "classes.dex")

# Step F: zipalign
print("7. Aligning APK with zipalign...")
ALIGNED_APK = os.path.join(BUILD_DIR, "aligned.apk")
cmd_zipalign = f'"{ZIPALIGN}" -f -p 4 "{UNALIGNED_APK}" "{ALIGNED_APK}"'
res = subprocess.run(cmd_zipalign, shell=True, capture_output=True, text=True)
if res.returncode != 0:
    print("Zipalign Error:", res.stderr)
    exit(1)

# Step G: Keystore & Apksigner
KEYSTORE = os.path.join(BUILD_DIR, "philip_release.jks")
KEY_PASS = "philip2026"
ALIAS = "philipfaceai"

print("8. Generating secure cryptographic release keystore...")
cmd_keytool = (
    f'"{KEYTOOL}" -genkey -v -keystore "{KEYSTORE}" -storepass {KEY_PASS} '
    f'-alias {ALIAS} -keypass {KEY_PASS} -keyalg RSA -keysize 2048 -validity 10000 '
    f'-dname "CN=Philip Antwi, OU=Faculty of Computing, O=Pentecost University, L=Accra, C=GH"'
)
res = subprocess.run(cmd_keytool, shell=True, capture_output=True, text=True)
if res.returncode != 0:
    print("Keytool Error:", res.stderr)
    exit(1)

print("9. Digitally signing APK with apksigner...")
cmd_sign = (
    f'"{JAVA_EXE}" -jar "{APKSIGNER_JAR}" sign --ks "{KEYSTORE}" --ks-pass pass:{KEY_PASS} '
    f'--key-pass pass:{KEY_PASS} --ks-key-alias {ALIAS} '
    f'--v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true '
    f'--out "{OUTPUT_APK}" "{ALIGNED_APK}"'
)
res = subprocess.run(cmd_sign, shell=True, capture_output=True, text=True)
if res.returncode != 0:
    print("Apksigner Error:", res.stderr)
    exit(1)

print(f"\n🎉 SUCCESS! Built and digitally signed Android APK:")
print(f"👉 Location: {OUTPUT_APK}")
print(f"👉 File Size: {os.path.getsize(OUTPUT_APK) / 1024:.1f} KB")
