Name:           box64
Version:        0.2.2
Release:        1%{?dist}
Summary:        Linux Userspace x86_64 Emulator

License:        MIT
URL:            https://github.com/ptitSeb/box64
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Only relevant on 64bit arm
ExclusiveArch:  aarch64

BuildRequires:  gcc-c++
BuildRequires:  cmake

%description
Linux Userspace x86_64 Emulator with a twist, targeted at ARM64 Linux devices.

%prep
%autosetup

# Fix perms
find . -type f -name *.c -exec chmod -x {} ';'
find . -type f -name *.h -exec chmod -x {} ';'
find . -type f -name *.S -exec chmod -x {} ';'
chmod -x LICENSE

%build
%cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DNOGIT=1 \
%if 0%{?_with_dynarec}
  -DARM_DYNAREC=1 \
%endif

%cmake_build

%install
%cmake_install

# Switch to system config and use correct path
mv %{buildroot}%{_sysconfdir}/binfmt.d %{buildroot}%{_prefix}/lib/binfmt.d
sed -i -e 's|/usr/local|/usr|' %{buildroot}%{_prefix}/lib/binfmt.d/box64.conf

%{?_with_tests:
%check
# Tests are failing for now as box64 isn't registered in binfmt.d
%ctest
}

%files
%license LICENSE 
%{_prefix}/lib/binfmt.d/box64.conf
%{_bindir}/box64
%ifnarch %{x86_64}
%{_prefix}/lib/x86_64-linux-gnu/libgcc_s.so.1
%{_prefix}/lib/x86_64-linux-gnu/libstdc++.so.5
%{_prefix}/lib/x86_64-linux-gnu/libstdc++.so.6
%{_prefix}/lib/x86_64-linux-gnu/libpng12.so.0
%endif

%changelog
* Tue Mar 21 2023 Robert Zaage <robert@zaage.it> - 0.2.2-1
- Initial release of version 0.2.2
