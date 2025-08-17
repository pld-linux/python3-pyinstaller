#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	pyinstaller
Summary:	PyInstaller bundles a Python application and all its dependencies into a single package
Name:		python3-%{module}
Version:	6.15.0
Release:	0.1
License:	GPL v2
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/p/pyinstaller/%{module}-%{version}.tar.gz
# Source0-md5:	9870de7e52f3be9ac85e3aef9a5fa5c0
Patch0:		bad-tests.patch
URL:		https://pyinstaller.org/
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools >= 42.0.0
%if %{with tests}
BuildRequires:	python3-altgraph
#BuildRequires:	python3-idlelib
BuildRequires:	python3-packaging >= 22.0
BuildRequires:	python3-pillow-qt
BuildRequires:	python3-psutil
BuildRequires:	python3-pyinstaller-hooks-contrib >= 2025.8
BuildRequires:	python3-pytest-timeout
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinxcontrib-towncrier
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
ExclusiveArch:	%{x8664} %{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyInstaller bundles a Python application and all its dependencies into
a single package. The user can run the packaged app without installing
a Python interpreter or any modules

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}
%patch -P0 -p1

# Needs graphics env
%{__rm} tests/functional/test_{qt,splash}.py

%build
%py3_build

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=timeout \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py3_sitedir}

%py3_install

# This is arch-dependant, why it installs to py3_sitescriptdir?
%{__mv} $RPM_BUILD_ROOT%{py3_sitescriptdir}/{PyInstaller,%{module}-%{version}-py*.egg-info} $RPM_BUILD_ROOT%{py3_sitedir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING.txt README.rst
%attr(755,root,root) %{_bindir}/pyi-archive_viewer
%attr(755,root,root) %{_bindir}/pyi-bindepend
%attr(755,root,root) %{_bindir}/pyi-grab_version
%attr(755,root,root) %{_bindir}/pyi-makespec
%attr(755,root,root) %{_bindir}/pyi-set_version
%attr(755,root,root) %{_bindir}/pyinstaller
%dir %{py3_sitedir}/PyInstaller
%{py3_sitedir}/PyInstaller/*.py
%{py3_sitedir}/PyInstaller/__pycache__
%{py3_sitedir}/PyInstaller/archive
%dir %{py3_sitedir}/PyInstaller/bootloader
%dir %{py3_sitedir}/PyInstaller/bootloader/Darwin-64bit
%attr(755,root,root) %{py3_sitedir}/PyInstaller/bootloader/Darwin-64bit/run*
%ifarch %{ix86}
%dir %{py3_sitedir}/PyInstaller/bootloader/Linux-32bit-intel
%attr(755,root,root) %{py3_sitedir}/PyInstaller/bootloader/Linux-32bit-intel/run*
%endif
%ifarch %{x8664}
%dir %{py3_sitedir}/PyInstaller/bootloader/Linux-64bit-intel
%attr(755,root,root) %{py3_sitedir}/PyInstaller/bootloader/Linux-64bit-intel/run*
%endif
%dir %{py3_sitedir}/PyInstaller/bootloader/Windows-32bit-intel
%attr(755,root,root) %{py3_sitedir}/PyInstaller/bootloader/Windows-32bit-intel/run*.exe
%dir %{py3_sitedir}/PyInstaller/bootloader/Windows-64bit-intel
%attr(755,root,root) %{py3_sitedir}/PyInstaller/bootloader/Windows-64bit-intel/run*.exe
%{py3_sitedir}/PyInstaller/bootloader/images
%{py3_sitedir}/PyInstaller/building
%{py3_sitedir}/PyInstaller/depend
%{py3_sitedir}/PyInstaller/fake-modules
%{py3_sitedir}/PyInstaller/hooks
%{py3_sitedir}/PyInstaller/isolated
%{py3_sitedir}/PyInstaller/lib
%{py3_sitedir}/PyInstaller/loader
%{py3_sitedir}/PyInstaller/utils
%{py3_sitedir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/*
%endif
