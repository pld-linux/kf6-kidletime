#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.8
%define		qtver		5.15.2
%define		kfname		kidletime

Summary:	Reporting of idle time of user and system
Name:		kf6-%{kfname}
Version:	6.8.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	593ae4b601369f10e9f1df7ed77e24b7
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6WaylandClient-devel
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-plasma-wayland-protocols-devel
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KIdleTime is a singleton reporting information on idle time. It is
useful not only for finding out about the current idle time of the PC,
but also for getting notified upon idle time events, such as custom
timeouts, or user activity.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{_datadir}/qlogging-categories6/kidletime.categories
%ghost %{_libdir}/libKF6IdleTime.so.6
%attr(755,root,root) %{_libdir}/libKF6IdleTime.so.*.*
%dir %{_libdir}/qt6/plugins/kf6/org.kde.kidletime.platforms
%{_libdir}/qt6/plugins/kf6/org.kde.kidletime.platforms/KF6IdleTimeWaylandPlugin.so
%{_libdir}/qt6/plugins/kf6/org.kde.kidletime.platforms/KF6IdleTimeXcbPlugin0.so
%{_libdir}/qt6/plugins/kf6/org.kde.kidletime.platforms/KF6IdleTimeXcbPlugin1.so
%{_datadir}/qlogging-categories6/kidletime.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KIdleTime
%{_libdir}/cmake/KF6IdleTime
%{_libdir}/libKF6IdleTime.so
