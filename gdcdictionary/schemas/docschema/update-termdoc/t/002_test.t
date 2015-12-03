use Test::More;
use Test::Exception;
use lib '../lib';

use_ok 'GDC::Docs::UpdateTerms';

my $wd = -d 't' ? '.' : '..';

my $creds = $ENV{DRUPAL_USER} && $ENV{DRUPAL_PASS};

SKIP : {
  skip 'credentials not specified', 4 unless $creds;
  my $upd;
  $upd = GDC::Docs::UpdateTerms->new( config_file => join('/',$wd,'conf','config.yaml') );
  ok $upd->login(), 'Logged in';
  ok !$upd->load_dict_page(term => 'Gefullte Fish'), 'couldn\'t find Gefullte Fish';
  ok $upd->load_dict_page(term => 'Aliquot'), 'got Aliquot';

  ok $upd->create_dict_page(term => 'Frelb'), 'created Frelb';
  CLEANUP : {
    if ($upd->mech->uri =~ /frelb/) {
      $upd->mech->follow_link( url_regex => qr|node/[0-9]+/edit| );
      $upd->mech->click( { id => 'edit-delete' } );
      $upd->mech->click( { id => 'edit-submit' } ) if $upd->mech->uri =~ /delete$/;
    }
  }
  1;
}
done_testing;
