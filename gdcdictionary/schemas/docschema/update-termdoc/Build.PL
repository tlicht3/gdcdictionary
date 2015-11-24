use Module::Build;

$build = Module::Build->new(
  dist_name => 'GDC-Docs-UpdateTerms',
  dist_version_from => 'lib/GDC/Docs/UpdateTerms.pm',
  perl => '5.18',
  requires => {
    'WWW::Mechanize::Firefox' => 0,
    'Config::Any' => 0,
    'Try::Tiny' => 0
   },
  build_requires => {
    'Test::More' => 0,
    'Test::Exception' => 0
   },
  configure_requires => {
    'Module::Build' => 0
    }
 );

$build->create_build_script;
