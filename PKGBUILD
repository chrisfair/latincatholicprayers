pkgname=latinprayermemorizer
pkgver=1.3.7
pkgrel=1
pkgdesc="A program to allow the memorization of Latin Catholic prayers."
arch=('any')
url="https://github.com/chrisfair/latincatholicprayers"
license=('GPL')
groups=()
depends=('python2' 'wxpython' 'python2-pygame' )
source=("https://launchpad.net/${pkgname}/stable/${pkgver}/+download/${pkgname}-${pkgver}.tar.gz"
	'version.patch'
        'configparser_api_changes.patch')
md5sums=('522ac80fef7123875271b30298ed6877'
         '847ae2478ae5e35f6e1af49aa9fb3fa9'
         '8e751e821558c989ac02ef687a7b7339')

build() {
	cd "${srcdir}/${pkgname}-${pkgver}"
	patch -p1 < "${srcdir}/version.patch"
        patch -p1 < "${srcdir}/configparser_api_changes.patch"
}

package() {
	cd "${srcdir}/${pkgname}-${pkgver}"
	python3 setup.py install --root ${pkgdir}
}



