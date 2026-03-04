%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

Name:           wgtunnel
Version:        1.0.0
Release:        1%{?dist}
Summary:        WireGuard and AmneziaWG VPN client with auto-tunneling, lockdown and proxying
License:        MIT
URL:            https://wgtunnel.com
ExclusiveArch:  x86_64

Source0:        https://github.com/wgtunnel/desktop/releases/download/%{version}/wgtunnel-%{version}-linux-amd64.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  gtk3

Requires:       gtk3
Requires:       iproute
Requires:       nftables
Requires:       libsecret

Requires(post): desktop-file-utils

Recommends:     libnotify
Suggests:       gnome-keyring
Suggests:       kwallet

%description
WireGuard and AmneziaWG VPN client with auto-tunneling, lockdown, and proxying.

%prep
%setup -q

%install
install -d %{buildroot}/usr/lib/wgtunnel
cp -a bin lib share %{buildroot}/usr/lib/wgtunnel/

# Symlinks in PATH
install -d %{buildroot}%{_bindir}
ln -sf /usr/lib/wgtunnel/bin/wgtunnel %{buildroot}%{_bindir}/wgtunnel
ln -sf /usr/lib/wgtunnel/bin/wgtctl   %{buildroot}%{_bindir}/wgtctl

# Desktop entry
install -d %{buildroot}%{_datadir}/applications
desktop="%{buildroot}%{_datadir}/applications/com.zaneschepke.wireguardautotunnel.wgtunnel.desktop"
if [ -f share/applications/com.zaneschepke.wireguardautotunnel.wgtunnel.desktop ]; then
    install -p -m 644 share/applications/com.zaneschepke.wireguardautotunnel.wgtunnel.desktop "$desktop"
    sed -i "s|^Exec=.*|Exec=wgtunnel|" "$desktop"
    sed -i "s|^Icon=.*|Icon=wgtunnel|" "$desktop"
fi

# Icons
if [ -d share/icons/hicolor ]; then
    install -d %{buildroot}%{_datadir}/icons/hicolor
    cp -a share/icons/hicolor/. %{buildroot}%{_datadir}/icons/hicolor/
fi

# Metainfo
install -d %{buildroot}%{_datadir}/metainfo
cp -f share/metainfo/*.metainfo.xml %{buildroot}%{_datadir}/metainfo/ 2>/dev/null || :

# Systemd service
install -D -m 644 lib/systemd/system/wgtunnel-daemon.service \
    %{buildroot}%{_unitdir}/wgtunnel-daemon.service

sed -i 's|ExecStart=.*|ExecStart=/usr/lib/wgtunnel/bin/daemon|' \
    %{buildroot}%{_unitdir}/wgtunnel-daemon.service
sed -i 's|WorkingDirectory=.*|WorkingDirectory=/usr/lib/wgtunnel|' \
    %{buildroot}%{_unitdir}/wgtunnel-daemon.service

%post
chmod +x /usr/lib/wgtunnel/bin/* 2>/dev/null || true
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :

echo "Updating icon cache..."
gtk-update-icon-cache -f /usr/share/icons/hicolor 2>/dev/null || true
update-desktop-database /usr/share/applications 2>/dev/null || true

cat << 'EOF'

=== WG Tunnel Installed Successfully ===

For KDE users: log out and back in (or restart plasmashell) to see the app icon.

Enable and start the daemon with:

    sudo systemctl enable --now wgtunnel-daemon.service

EOF

%preun
if [ $1 -eq 0 ]; then
    /usr/bin/systemctl --no-block stop wgtunnel-daemon.service >/dev/null 2>&1 || :
    /usr/bin/systemctl disable wgtunnel-daemon.service >/dev/null 2>&1 || :
fi

%postun
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%{_bindir}/wgtunnel
%{_bindir}/wgtctl
/usr/lib/wgtunnel
%{_datadir}/applications/com.zaneschepke.wireguardautotunnel.wgtunnel.desktop
%{_datadir}/icons/hicolor/*
%{_datadir}/metainfo/*.metainfo.xml
%{_unitdir}/wgtunnel-daemon.service

%changelog
* Wed Mar 04 2026 Zane Schepke <support@wgtunnel.com> - 1.0.0-1
- Initial release