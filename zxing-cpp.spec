#
# Conditional build:
%bcond_without	opencv		# OpenCV interface
#
Summary:	C++ port of ZXing - 1D/2D barcode image processing library
Summary(pl.UTF-8):	Port C++ biblioteki ZXing, przetwarzającej kody paskowe 1D/2D
Name:		zxing-cpp
# no version information in sources; cpp port has been removed from zxing repository between 2.3.0 and 3.0.0 releases
Version:	2.3.0
%define	gitref	6b3cbe02a332bff0f5ba0416f221d3d3876afdc2
%define	snap	20161123
Release:	0.%{snap}.1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/glassechidna/zxing-cpp/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	14a1766c04ac825fc588c03b2fb04be1
Patch0:		%{name}-cmake.patch
URL:		https://github.com/glassechidna/zxing-cpp
BuildRequires:	cmake >= 2.8.0
BuildRequires:	libstdc++-devel
%{?with_opencv:BuildRequires:	opencv-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C++ port of ZXing - 1D/2D barcode image processing library.

%description -l pl.UTF-8
Port C++ biblioteki ZXing, przetwarzającej kody paskowe 1D/2D

%package devel
Summary:	Header files for ZXing library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ZXing
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for ZXing library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ZXing.

%package opencv
Summary:	OpenCV/ZXing based QR code recognizer
Summary(pl.UTF-8):	Program do rozpoznawania kodów QR oparty na bibliotekach OpenCV/ZXing
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description opencv
OpenCV/ZXing based QR code recognizer.

%description opencv -l pl.UTF-8
Program do rozpoznawania kodów QR oparty na bibliotekach OpenCV/ZXing.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_opencv:-DOpenCV_FOUND=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with opencv}
# API (opencv/src/zxing/MatSource.h) not installed
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzxing-cv.so
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	opencv -p /sbin/ldconfig
%postun	opencv -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_bindir}/zxing
%attr(755,root,root) %{_libdir}/libzxing.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzxing.so
%{_includedir}/zxing

%if %{with opencv}
%files opencv
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzxing-cv.so.0
%attr(755,root,root) %{_bindir}/zxing-cv
%endif
