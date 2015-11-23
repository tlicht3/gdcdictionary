use Test::More;
use Test::Exception;
use lib '../lib';

use_ok 'GDC::Docs::UpdateTerms';

my $wd = -d 't' ? '.' : '..';

my $creds = $ENV{DRUPAL_USER} && $ENV{DRUPAL_PASS};

SKIP : {
  skip 'credentials not specified', 4 unless $creds;
  my $upd;
  lives_ok {
    $upd = GDC::Docs::UpdateTerms->new( config_file => join('/',$wd,'conf','config.yaml') );
  };
  isa_ok($upd, 'GDC::Docs::UpdateTerms');
  is $upd->site_url, 'https://gdc-dev.nci.nih.gov';
  is $upd->dict_url, 'https://gdc-dev.nci.nih.gov/gdc-dictionary';
  $pass = $upd->{p};
  $upd->{p} = 'goob';
  ok !$upd->login(), 'bad creds, login failed';
  $upd->{p} = $pass;
  ok $upd->login(), 'good creds, login succeeds';
}
done_testing;
