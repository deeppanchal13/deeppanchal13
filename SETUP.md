# SETUP GUIDE - Deep Panchal's GitHub Profile

This guide is written for beginners. Follow the steps in order.

---

## 1. Where to put the files

The profile README only works from a **special repository** whose name is exactly your username:

```
deeppanchal13/deeppanchal13
```

Everything in this folder goes into the **root** of that repository:

```
deeppanchal13/               <- the repository
├── README.md                <- the profile page people see
├── SETUP.md                 <- this guide (you may delete it later)
├── .github/
│   └── workflows/
│       └── profile-3d.yml  <- the automatic 3D-graph updater
├── assets/                  <- pixel-art SVGs (header, section titles, icons)
├── profile-3d-contrib/
│   └── profile-night-green.svg   <- placeholder, replaced by the workflow
└── tools/
    └── generate_assets.py   <- optional: re-generates the pixel-art SVGs
```

Note: `.github` starts with a dot. Make sure your file explorer shows hidden folders, and that the folder is uploaded.

## 2. Create / use the profile repository

1. Go to <https://github.com/new>.
2. **Repository name:** `deeppanchal13` (must match your username exactly).
3. Set it to **Public**. Tick **Add a README file** only if you want; you will overwrite it anyway.
4. Upload all the files from this folder (drag and drop on the GitHub web page works, or use `git push`).
   The default branch should be `main`.
5. Open your profile (<https://github.com/deeppanchal13>). The README now appears.

## 3. Make the 3D graph real (do this once, right away)

The file `profile-3d-contrib/profile-night-green.svg` in this package is only a **placeholder** that says "waiting for first run". It contains no data. Replace it with your real graph:

1. Open your repository on GitHub -> **Actions** tab.
2. If GitHub asks, click **"I understand my workflows, go ahead and enable them"**.
3. Click **GitHub-Profile-3D-Contrib** in the left list.
4. Click **Run workflow** -> **Run workflow** (green button).
5. Wait about a minute until the run shows a green tick.
6. Refresh your profile. The real 3D contribution graph, activity radar, language donut and totals are now shown.

## 4. How the GitHub Action works

`.github/workflows/profile-3d.yml` does three things each time it runs:

1. **Checks out** your repository.
2. Runs [`yoshi389111/github-profile-3d-contrib`](https://github.com/yoshi389111/github-profile-3d-contrib) (pinned to version `0.7.1`), which reads your real GitHub contributions and writes several SVG files into `profile-3d-contrib/`.
3. **Commits and pushes** those SVGs, but only if something changed (so no empty commits).

Safety details already handled for you:

- `permissions: contents: write` lets the workflow push.
- There is **no `push` trigger**, and pushes made with the built-in token never start new runs, so it cannot loop.
- `concurrency` stops two runs from fighting each other.

The README uses the `profile-night-green.svg` variant (dark, green blocks). Other variants are generated too, in the same folder. To switch, change the file name in `README.md`, for example:

| File | Look |
| --- | --- |
| `profile-night-green.svg` | dark + green (used) |
| `profile-green.svg` / `profile-green-animate.svg` | light-ground green / animated |
| `profile-night-view.svg` | dark, original GitHub colors |
| `profile-night-rainbow.svg` | dark, rainbow |
| `profile-gitblock.svg` | git-block style |

## 5. Run it manually

GitHub -> your repo -> **Actions** -> **GitHub-Profile-3D-Contrib** -> **Run workflow**.

## 6. How automatic updates work

```
You contribute on GitHub
        |
GitHub records your activity
        |
Scheduled Action runs (every 12 hours, 17 minutes past)
        |
3D SVG is regenerated from your real data
        |
Changed SVG is committed to the repo
        |
README shows the updated graph
```

You never edit the README for this. Things to know:

- The schedule is in UTC and can be delayed by GitHub at busy times. That is normal.
- The graph updates at most every 12 hours. Use **Run workflow** for an instant refresh.
- GitHub may pause scheduled workflows in repos with no activity for 60 days. Because the workflow commits whenever your graph changes, this normally will not happen. If it does, just click **Enable workflow** in the Actions tab.
- The cards below the 3D graph (stats, streak, top languages, activity graph) are loaded live from online services and have their own caching, so they can lag a few hours.
- **Private contributions** are not counted by default. To include them, create a Personal Access Token (classic, scopes `repo` and `read:user`), save it as a repository secret named `PROFILE_TOKEN` (Settings -> Secrets and variables -> Actions), then in `profile-3d.yml` change `GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}` to `GITHUB_TOKEN: ${{ secrets.PROFILE_TOKEN }}`. This is optional.

## 7. Replace the LinkedIn / email / portfolio placeholders

Open `README.md` and use find-and-replace (in the GitHub editor press `Ctrl+F` / `Cmd+F`, or use your code editor):

| Find | Replace with | Example |
| --- | --- | --- |
| `LINKEDIN_PLACEHOLDER` | your LinkedIn username | `deep-panchal-123` |
| `EMAIL_PLACEHOLDER` | the part of your Gmail before `@gmail.com` | `yourname` |
| `PORTFOLIO_PLACEHOLDER` | your site, without `https://` | `deeppanchal.dev` |

Each placeholder appears twice (once in the icon row near the top, once in the CONNECT section), so use "replace all".
If you do not have one of them yet, delete that icon cell and badge instead of leaving a fake link.

## 8. Change skills

In `README.md`, find `SKILL SET`. Every skill is one `<td>` cell:

```html
<td align="center" width="20%"><img src="https://skillicons.dev/icons?i=react&theme=dark" width="48" height="48" alt="React"><br><sub><b>React</b></sub></td>
```

- **Add a skill:** copy a cell, change `i=react` to another icon id (list at <https://skillicons.dev>) and change the label. Keep 5 cells per `<tr>` row.
- **Remove a skill:** delete its `<td>...</td>`.
- **Move "learning" to "current":** cut the `<td>` and paste it into the CURRENT table.
- **Empty "next" slots** use `./assets/slot-empty.svg`; replace one with a real skill when you learn it.
- `DSA` and `Backend Dev` have no official icon, so they use small custom icons in `assets/`.

## 9. Add a new project

Copy one project `<td>` block in the PROJECTS section and edit the text:

```html
<td width="50%" valign="top">
  <b><code>06</code> PROJECT NAME</b><br>
  One or two sentences about what it does.<br><br>
  <img src="https://img.shields.io/badge/React-0f2a14?style=flat-square&logo=react&logoColor=00ff66" alt="React">
  <br><a href="https://github.com/deeppanchal13/REPO_NAME">Repo</a> | <a href="https://YOUR_DEMO_URL">Demo</a>
</td>
```

- Replace the `NEXT_BUILD.exe` cell with your new project.
- Add the `Repo` / `Demo` line **only when the real link exists**.
- Tag format: `https://img.shields.io/badge/TEXT-0f2a14?style=flat-square&logo=ICON&logoColor=00ff66`. Use `_` for spaces and `%2B` for `+`. Icon names: <https://simpleicons.org>.

## 10. Customize colors and design

Colors: all pixel-art SVGs come from one script.

1. Open `tools/generate_assets.py`. The color list is at the top (`GREEN`, `BG`, `PANEL`, ...).
2. Change values, then run: `python tools/generate_assets.py` (needs Python 3, nothing to install).
3. Commit the updated files in `assets/`.

Section titles: edit the `SECTIONS` list in the same script (the pixel font supports A-Z, 0-3, `-`, `/`, `.` and space; add more glyphs in the `F` table if you need them).

The stats cards below the 3D graph use hex colors in their URLs (`bg_color=0b120b`, `title_color=00ff66`, ...). Change them there. The 3D graph itself keeps the generator's own palette; try a different variant (see section 4).

## 11. If the workflow fails

Open **Actions** -> click the red run -> click the failed step to read the message.

| Problem | Fix |
| --- | --- |
| `Permission denied` / `403` when pushing | Settings -> Actions -> General -> **Workflow permissions** -> select **Read and write permissions** -> Save. Re-run. |
| Workflow does not appear in Actions | The file must be exactly `.github/workflows/profile-3d.yml` on the default branch. Check the folder names and the leading dot. |
| Actions disabled | Actions tab -> enable workflows. Settings -> Actions -> General -> allow actions. |
| Graph still shows "waiting for first run" | Run the workflow manually (section 3) and check it finished green. Hard-refresh the page (`Ctrl+Shift+R`); GitHub caches images for a few minutes. |
| Repo name is wrong, nothing shows on profile | The repo must be named exactly `deeppanchal13` and be public. |
| Git push rejected (non-fast-forward) | Just run the workflow again. |
| Action itself errors (old Node warning or similar) | Check <https://github.com/yoshi389111/github-profile-3d-contrib/releases> for a newer version and update the `@0.7.1` tag in the workflow. Also bump `actions/checkout@v4` if GitHub deprecates it. |
| A stats card shows an error or "rate limit" | Those cards are free public services and are sometimes overloaded. Wait and refresh. If it persists, deploy your own copy of [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) on Vercel and replace the domain in the URLs, or remove that card. |
| An image is broken in the README | Right-click it -> open image in new tab to see the exact URL, then compare with the file name in `assets/`. File names are case-sensitive. |

Still stuck? Copy the red error text from the Actions log and search for it, or ask for help with it.
