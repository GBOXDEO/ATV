name: build

on: 
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Run build with Gradle wrapper
        run: |
          chmod +x gradlew
          ./gradlew assembleRelease -PIS_SO_BUILD=false

      - name: Prepare App
        run: |
          mkdir -p ${{ github.workspace }}/apk/
          for file in `find ~ -name "*.apk" -print`; do
            mv "$file" ${{ github.workspace }}/apk/
          done
      - name: Upload App To Artifact
        uses: actions/upload-artifact@v3
        with:
          name: my-tv-${{ github.ref_name }}.apk
          path: ${{ github.workspace }}/apk/*
