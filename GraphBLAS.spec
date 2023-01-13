# TODO: CUDA
#
# Conditional build:
%bcond_without	openmp		# OpenMP support
%bcond_with	static_libs	# static libraries
#
Summary:	SuiteSparse:GraphBLAS - complete implementation of the GraphBLAS standard
Summary(pl.UTF-8):	SuiteSparse:GraphBLAS - pełna implementacja standardu GraphBLAS
Name:		GraphBLAS
Version:	7.4.1
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/DrTimothyAldenDavis/GraphBLAS/releases
Source0:	https://github.com/DrTimothyAldenDavis/GraphBLAS/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d2379bca33b609dba3bbc193dfd6eb00
URL:		http://faculty.cse.tamu.edu/davis/GraphBLAS.html
BuildRequires:	cmake >= 3.19
BuildRequires:	gcc >= 6:4.9
BuildRequires:	libatomic-devel
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	rpm-build >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SuiteSparse:GraphBLAS is a complete implementation of the GraphBLAS
standard, which defines a set of sparse matrix operations on an
extended algebra of semirings using an almost unlimited variety of
operators and types. When applied to sparse adjacency matrices, these
algebraic operations are equivalent to computations on graphs.
GraphBLAS provides a powerful and expressive framework for creating
graph algorithms based on the elegant mathematics of sparse matrix
operations on a semiring.

%description -l pl.UTF-8
SuiteSparse:GraphBLAS to pełna implementacja standardu GraphBLAS,
definiującego zbiór operacji na macierzach rzadkich w rozszerzonej
algebrze półpierścieni przy użyciu nieograniczonej różnorodności
operatorów i typów. W odniesieniu do rzadkich macierzy sąsiedztwa te
operacje algebraiczne są równoważne obliczeniom na grafach. GraphBLAS
zapewnia potężny i ekspresyjny szkielet do tworzenia algorytmów
grafowych w oparciu o elegancką matematykę operacji na macierzach
rzadkich na półpierścieniu.

%package devel
Summary:	Header files for GraphBLAS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GraphBLAS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for GraphBLAS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GraphBLAS.

%package static
Summary:	Static GraphBLAS library
Summary(pl.UTF-8):	Statyczna biblioteka GraphBLAS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GraphBLAS library.

%description static -l pl.UTF-8
Statyczna biblioteka GraphBLAS.

%package apidocs
Summary:	API documentation for GraphBLAS library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GraphBLAS
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for GraphBLAS library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GraphBLAS.

%prep
%setup -q

%build
%cmake -B build \
	-DGLOBAL_INSTALL=ON \
	%{!?with_openmp:-DNOPENMP=ON} \
	%{?with_static_libs:-DNSTATIC=OFF}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md Doc/ChangeLog
%attr(755,root,root) %{_libdir}/libgraphblas.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgraphblas.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgraphblas.so
%{_includedir}/GraphBLAS.h
%dir %{_libdir}/cmake/SuiteSparse
%{_libdir}/cmake/SuiteSparse/FindGraphBLAS.cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgraphblas.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc Doc/{CSC20_OpenMP_GraphBLAS.pdf,Davis_HPEC18.pdf,GraphBLAS_API_C_2.0.0.pdf,GraphBLAS_API_C_v13.pdf,HPEC19.pdf}
%endif
