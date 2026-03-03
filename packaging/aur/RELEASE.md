# AUR Release Checklist

1. Update PKGBUILD: pkgver, sha256sums
2. Test locally
3. Update .SRCINFO
4. Commit & push to AUR

**Test**
```bash
makepkg -si
```

**Generate .SRCINFO**
```bash
makepkg --printsrcinfo > .SRCINFO
```

**Push to AUR**
```bash
git add PKGBUILD wgtunnel-bin.install .SRCINFO
git commit -m <message>
git push origin master
```