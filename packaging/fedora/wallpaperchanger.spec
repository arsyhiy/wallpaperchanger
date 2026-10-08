Name:           wallpaperchanger
Version:        0.1.0
Release:        1%{?dist}
Summary:        Linux wallpaper changer

License:        MIT
URL:            https://example.com/wallpaperchanger
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-dearpygui

%description
Wallpaper changer for Linux.

%prep
%autosetup

%build
%pyproject_wheel

%install
%pyproject_install

install -D -m 644 data/wallpaperchanger.desktop \
    %{buildroot}%{_datadir}/applications/wallpaperchanger.desktop

install -D -m 644 data/wallpaperchanger.service \
    %{buildroot}%{_userunitdir}/wallpaperchanger.service

%files
%license LICENSE
%doc README.md

%{_bindir}/wallpaperchanger
%{_bindir}/wallpaperchanger-service
%{_datadir}/applications/wallpaperchanger.desktop
%{_userunitdir}/wallpaperchanger.service
