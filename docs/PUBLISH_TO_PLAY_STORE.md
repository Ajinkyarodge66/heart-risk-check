# Publishing Heart Risk Check on Google Play

The app is already an installable web app (PWA). Google Play accepts PWAs wrapped as a **Trusted Web Activity**, and PWABuilder creates that package for you without Android Studio.

## Before you start
- The app must be live at `https://ajinkyarodge66.github.io/heart-risk-check/web/` (GitHub Pages).
- **Google Play developer account:** a one-time **US$25** fee, a government ID and an Android phone for verification.
- **New personal accounts** must run a **closed test with at least 12 testers for 14 days in a row** before they can publish to everyone. Start recruiting testers now: friends, classmates and family.

## Step 1: Check the app with PWABuilder
1. Go to https://www.pwabuilder.com and paste your app URL.
2. It scores the manifest, service worker and security. This version includes PNG icons, a maskable icon, screenshots, shortcuts and offline support, so it should pass.

## Step 2: Generate the Android package
1. Click **Package for stores**, choose **Android**, then **Generate**.
2. Package ID: for example `io.github.ajinkyarodge66.heartriskcheck`.
3. Download the zip. It contains the `.aab` file for Google Play, a **signing key**, and an `assetlinks.json` file.
4. ⚠️ **Back up the signing key and its passwords somewhere safe.** If you lose them, you can never update the app.

## Step 3: Remove the browser address bar (Digital Asset Links)
Android only hides the address bar if `assetlinks.json` is served from the root of your domain, at `https://ajinkyarodge66.github.io/.well-known/assetlinks.json`.
1. Create a new public GitHub repository named exactly **`ajinkyarodge66.github.io`**.
2. Inside it, create a folder `.well-known` and put the `assetlinks.json` from PWABuilder in it.
3. Add an empty file called `.nojekyll` at the root. Without it, GitHub Pages hides folders that start with a dot.
4. Turn on Pages for that repository (main branch, root).

If you skip this step the app still works, but it shows a small address bar at the top.

## Step 4: Play Console
1. Go to https://play.google.com/console, create the app, and choose **Health & Fitness**.
2. Copy the store text from `docs/store/play-store-listing.md`.
3. Upload the screenshots from `web/screenshots/` and use `web/icon-512.png` as the app icon.
4. Fill in the **Data safety** form and the **Health apps** declaration, using the suggested answers in the listing file.
5. Privacy policy URL: `https://ajinkyarodge66.github.io/heart-risk-check/web/privacy.html`
6. **Testing → Closed testing:** upload the `.aab`, add your 12 or more testers, and keep them opted in for 14 days.
7. Then apply for production access. Google's review usually takes about a week.

## iPhone
iPhone users can already install the app from Safari: tap **Share**, then **Add to Home Screen**. A real App Store listing needs an Apple Developer account and a native wrapper, so leave it until after Android.
