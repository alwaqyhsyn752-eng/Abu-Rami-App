#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مولّد بنية APK Builder — يضيف كل ملفات أندرويد + GitHub Actions + خدمة البناء
"""

import os

FILES = {}

# ============================================================
# android_template/settings.gradle
# ============================================================
FILES["android_template/settings.gradle"] = r"""pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "AbuRamiApp"
include ':app'
"""

# ============================================================
# android_template/build.gradle
# ============================================================
FILES["android_template/build.gradle"] = r"""plugins {
    id 'com.android.application' version '8.2.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.20' apply false
}
"""

# ============================================================
# android_template/gradle.properties
# ============================================================
FILES["android_template/gradle.properties"] = r"""org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
kotlin.code.style=official
"""

# ============================================================
# android_template/app/build.gradle
# ============================================================
FILES["android_template/app/build.gradle"] = r"""plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.aburami.generated'
    compileSdk 34

    defaultConfig {
        applicationId "com.aburami.generated"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    signingConfigs {
        release {
            storeFile file("../release.keystore")
            storePassword "aburami123"
            keyAlias "aburami"
            keyPassword "aburami123"
        }
    }

    buildTypes {
        release {
            minifyEnabled false
            signingConfig signingConfigs.release
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = '17'
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.webkit:webkit:1.9.0'
}
"""

# ============================================================
# AndroidManifest.xml
# ============================================================
FILES["android_template/app/src/main/AndroidManifest.xml"] = r"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />

    <application
        android:allowBackup="true"
        android:label="__APP_NAME__"
        android:icon="@mipmap/ic_launcher"
        android:supportsRtl="true"
        android:usesCleartextTraffic="true"
        android:theme="@style/AppTheme">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

# ============================================================
# MainActivity.kt
# ============================================================
FILES["android_template/app/src/main/java/com/aburami/generated/MainActivity.kt"] = r"""package com.aburami.generated

import android.os.Bundle
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        webView = WebView(this)
        setContentView(webView)

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true
            mediaPlaybackRequiresUserGesture = false
            allowFileAccess = true
            cacheMode = WebSettings.LOAD_DEFAULT
        }

        webView.webViewClient = WebViewClient()

        webView.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest?) {
                request?.grant(request.resources)
            }
        }

        webView.loadUrl("file:///android_asset/index.html")
    }

    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) {
            webView.goBack()
        } else {
            @Suppress("DEPRECATION")
            super.onBackPressed()
        }
    }
}
"""

# ============================================================
# strings.xml
# ============================================================
FILES["android_template/app/src/main/res/values/strings.xml"] = r"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">__APP_NAME__</string>
</resources>
"""

# ============================================================
# themes.xml
# ============================================================
FILES["android_template/app/src/main/res/values/themes.xml"] = r"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.DayNight.NoActionBar">
        <item name="android:windowBackground">@android:color/black</item>
        <item name="android:statusBarColor">@android:color/black</item>
        <item name="android:navigationBarColor">@android:color/black</item>
    </style>
</resources>
"""

# ============================================================
# assets/index.html (placeholder)
# ============================================================
FILES["android_template/app/src/main/assets/index.html"] = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>App</title></head>
<body><h1>Placeholder — will be replaced at build time</h1></body>
</html>
"""

# ============================================================
# android_template/.gitignore
# ============================================================
FILES["android_template/.gitignore"] = r""".gradle/
build/
local.properties
*.iml
.idea/
release.keystore
"""

# ============================================================
# .github/workflows/build-apk.yml
# ============================================================
FILES[".github/workflows/build-apk.yml"] = r"""name: Build APK

on:
  workflow_dispatch:
    inputs:
      app_name:
        description: 'App display name'
        required: true
        type: string
      app_html_base64:
        description: 'Base64-encoded HTML content'
        required: true
        type: string
      build_id:
        description: 'Unique build ID'
        required: true
        type: string

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Java 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'

      - name: Set up Android SDK
        uses: android-actions/setup-android@v3

      - name: Set up Gradle
        uses: gradle/actions/setup-gradle@v4

      - name: Prepare project
        shell: bash
        run: |
          set -e
          BUILD_ID="${{ github.event.inputs.build_id }}"
          APP_NAME="${{ github.event.inputs.app_name }}"
          HTML_B64="${{ github.event.inputs.app_html_base64 }}"

          mkdir -p android_build
          cp -r android_template/. android_build/
          cd android_build

          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > release.keystore

          sed -i "s/__APP_NAME__/${APP_NAME}/g" app/src/main/AndroidManifest.xml
          sed -i "s/__APP_NAME__/${APP_NAME}/g" app/src/main/res/values/strings.xml
          sed -i "s/com\.aburami\.generated/com.aburami.${BUILD_ID}/g" app/build.gradle
          sed -i "s/package com\.aburami\.generated/package com.aburami.${BUILD_ID}/g" app/src/main/java/com/aburami/generated/MainActivity.kt

          echo "${HTML_B64}" | base64 -d > app/src/main/assets/index.html

      - name: Build Release APK
        working-directory: android_build
        run: gradle assembleRelease --no-daemon --stacktrace

      - name: Rename APK
        run: |
          mkdir -p output
          cp android_build/app/build/outputs/apk/release/app-release.apk \
             "output/${{ github.event.inputs.app_name }}.apk"

      - name: Upload APK to Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: apk-${{ github.event.inputs.build_id }}
          name: "APK — ${{ github.event.inputs.app_name }}"
          body: "Generated by Abu Rami AI"
          files: output/*.apk
          token: ${{ secrets.GITHUB_TOKEN }}
"""

# ============================================================
# app/services/apk_builder.py
# ============================================================
FILES["app/services/apk_builder.py"] = r"""import os
import base64
import asyncio
import logging
from typing import Optional
import httpx

logger = logging.getLogger(__name__)

GITHUB_OWNER = "alwaqyhsyn752-eng"
GITHUB_REPO = "Abu-Rami-App"
WORKFLOW_FILE = "build-apk.yml"


class APKBuilder:
    def __init__(self):
        self.token = os.getenv("GITHUB_ACTIONS_TOKEN", "").strip()
        if not self.token:
            logger.warning("GITHUB_ACTIONS_TOKEN not set - APK build disabled")

    async def trigger_build(
        self, app_name: str, html_content: str, build_id: str
    ) -> bool:
        if not self.token:
            raise RuntimeError("GITHUB_ACTIONS_TOKEN not configured")

        url = (
            "https://api.github.com/repos/"
            + GITHUB_OWNER + "/" + GITHUB_REPO
            + "/actions/workflows/" + WORKFLOW_FILE + "/dispatches"
        )

        headers = {
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        payload = {
            "ref": "main",
            "inputs": {
                "app_name": app_name,
                "app_html_base64": base64.b64encode(
                    html_content.encode("utf-8")
                ).decode("ascii"),
                "build_id": build_id,
            },
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, json=payload, headers=headers)
            if res.status_code not in (200, 204):
                raise RuntimeError(
                    "GitHub API: " + str(res.status_code) + " " + res.text[:200]
                )
            logger.info("APK build triggered: %s", build_id)
            return True

    async def poll_build(
        self, build_id: str, timeout: int = 20
    ) -> Optional[str]:
        if not self.token:
            return None

        headers = {
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
        }

        url = (
            "https://api.github.com/repos/"
            + GITHUB_OWNER + "/" + GITHUB_REPO
            + "/releases/tags/apk-" + build_id
        )

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                r = await client.get(url, headers=headers)
                if r.status_code == 200:
                    data = r.json()
                    for asset in data.get("assets", []):
                        name = asset.get("name", "")
                        if name.endswith(".apk"):
                            return asset.get("browser_download_url")
        except Exception as e:
            logger.warning("Poll failed: %s", e)

        return None


apk_builder = APKBuilder()
"""


def main():
    print("=" * 65)
    print("توليد بنية APK Builder لمشروع Abu-Rami-App")
    print("=" * 65)

    count = 0
    for path, content in FILES.items():
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content if content.endswith("\n") else content + "\n")
        print(" [+] " + path)
        count += 1

    # مولدات أيقونة PNG
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        import subprocess
        import sys
        print(" ... تثبيت Pillow لإنشاء الأيقونات")
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], check=True)
        from PIL import Image, ImageDraw

    sizes = {
        "mdpi": 48,
        "hdpi": 72,
        "xhdpi": 96,
        "xxhdpi": 144,
        "xxxhdpi": 192,
    }

    for name, size in sizes.items():
        dir_path = "android_template/app/src/main/res/mipmap-" + name
        os.makedirs(dir_path, exist_ok=True)
        img = Image.new("RGBA", (size, size), (2, 6, 23, 255))
        d = ImageDraw.Draw(img)
        cx = cy = size // 2
        r = int(size * 0.42)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(6, 182, 212, 255))
        r2 = int(size * 0.22)
        d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(2, 6, 23, 255))
        img.save(os.path.join(dir_path, "ic_launcher.png"))
        print(" [+] " + dir_path + "/ic_launcher.png")

    print("=" * 65)
    print("اكتمل! عدد الملفات: " + str(count + 5))
    print("=" * 65)


if __name__ == "__main__":
    main()
