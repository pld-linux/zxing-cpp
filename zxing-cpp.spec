#
# Conditional build:
%bcond_without	opencv		# OpenCV interface

%define	rel	1
Summary:	C++ port of ZXing - 1D/2D barcode image processing library
Summary(pl.UTF-8):	Port C++ biblioteki ZXing, przetwarzającej kody paskowe 1D/2D
Name:		zxing-cpp
# no version information in sources; cpp port has been removed from zxing repository between 2.3.0 and 3.0.0 releases
Version:	2.3.0
%define	gitref	e0e40ddec63f38405aca5c8c1ff60b85ec8b1f10
%define	snap	20190321
Release:	0.%{snap}.%{rel}
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/glassechidna/zxing-cpp/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	41d2af7fc424e1c6129192bd87d54c5f
Patch0:		%{name}-cmake.patch
Patch1:		no-opencv.patch
URL:		https://github.com/glassechidna/zxing-cpp
BuildRequires:	cmake >= 3.0
BuildRequires:	libstdc++-devel >= 6:4.7
%{?with_opencv:BuildRequires:	opencv-devel >= 2}
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
Requires:	libstdc++-devel >= 6:4.7

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

%package opencv-devel
Summary:	Header file for ZXing OpenCV library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki ZXing OpenCV
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-opencv = %{version}-%{release}
Requires:	opencv-devel >= 2

%description opencv-devel
Header file for ZXing OpenCV library.

%description opencv-devel -l pl.UTF-8
Plik nagłówkowy biblioteki ZXing OpenCV.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_opencv:-DUSE_OPENCV=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_libdir}/zxing/cmake/zxing-targets.cmake

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
%dir %{_includedir}/zxing
%{_includedir}/zxing/aztec
%{_includedir}/zxing/common
%{_includedir}/zxing/datamatrix
%{_includedir}/zxing/multi
%{_includedir}/zxing/oned
%{_includedir}/zxing/pdf417
%{_includedir}/zxing/qrcode
%{_includedir}/zxing/[!M]*.h
%{_includedir}/zxing/MultiFormatReader.h
%dir %{_libdir}/zxing
%{_libdir}/zxing/cmake

%if %{with opencv}
%files opencv
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zxing-cv
%attr(755,root,root) %{_libdir}/libzxing-cv.so.0

%files opencv-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzxing-cv.so
%{_includedir}/zxing/MatSource.h
%endif
