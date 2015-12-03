package GDC::Docs::UpdateTerms;
use WWW::Mechanize::Firefox;
use Config::Any;
use Try::Tiny;

use strict;
#use warnings;
our $VERSION='0.1';
$DB::deep=1000;

sub new {
  my $class = shift;
  my %args = @_;
  my $self = bless {}, $class;
  my $cfg;
  try {
    $cfg = Config::Any->load_files( { files => [ $args{config_file} || 'config.yaml' ], use_ext => 1 } );
    (my $fn, $self->{config}) = %{$cfg->[0]};
  } catch {
    1;
  };
  $self->{site_url} = $args{site_url} || $self->{config}->{site_url};
  $self->{dict_url} = $args{dict_url} || $self->{config}->{dict_url};
  die 'No config file or configuration specified in args' unless $self->{site_url};
  unless ($self->{dict_url} =~ /^https?:/) {
    $self->{dict_url} = join('/', $self->{site_url},$self->{dict_url});
    $self->{dict_url} =~ s{([^:])//}{$1/}g;
  }
  $self->{u} = $args{user} || $ENV{DRUPAL_USER};
  $self->{p} = $args{pass} || $ENV{DRUPAL_PASS};
  try {
    $self->{mech} = WWW::Mechanize::Firefox->new( ssl_opts => { SSL_fingerprint => $self->{config}{site_cert_fp} });
  } catch {
    die "Problem with Firefox: is it running? Did you turn on MozRepl (Tool->Mozrepl->Start)?";
  };
  
  return $self;
}

sub mech { shift->{mech} }
sub site_url { shift->{site_url} }
sub dict_url { shift->{dict_url} }

sub login {
  my $self = shift;
  # login if nec
  $self->mech->get( join('/',$self->site_url,'user') );
  unless ($self->mech->selector('span.username',any=>1)) {
    $self->mech->set_visible($self->{u},$self->{p});
    $self->mech->click({ id => 'edit-submit' });
  }
  return if $self->mech->content =~ /Sorry, unrecognized username/;
  return 1;
}

# nav
sub load_dict_page {
  my $self = shift;
  my %args = @_;
  my $term = $args{term};
  die "Need to specify term as 'term => Yourterm'" unless $term;
  $self->mech->get($self->dict_url);
  my $ret = 1;
  try {
    $self->mech->follow_link(text=>$term);
    1;
  } catch {
    $ret = 0;
  };
  return $ret;
}

sub create_dict_page {
  my $self = shift;
  my %args = @_;
  my $term = $args{term};
  die "Need to specify term as 'term => Yourterm'" unless $term;
  unless ($self->mech->uri eq $self->dict_url) {
    $self->mech->get($self->dict_url)
  }
  $self->mech->follow_link( url_regex => qr|/node/add/page| );
  # in new page
  $self->mech->field('#edit-title' => $term );
  $self->mech->by_id('edit-log',one=>1)->{textContent} = 'Created by GDC::Docs::UpdateTerm agent';
  # check Markdown
  my ($mdselect) = grep { $_->{textContent} =~ /Markdown/ } $self->mech->selector('label.option');
  $self->mech->click( { dom => $mdselect->{firstChild}, synchronize => 0 } );
  $self->mech->click( { id => 'edit-submit' } );
  return $self->mech->success;
}

sub update_page {
  my $self = shift;
  my ($content) = @_;
  my $l = $self->mech->find_link_dom( url_regex => qr|node/[0-9]+/edit|, one=>1 );
  $self->mech->follow_link($l);
  # replace text and submit
  my $textarea = $self->mech->by_id('edit-body',one=>1);
  $textarea->{textContent} = $content;
  $self->mech->click( { id => 'edit-submit' } );
  return $self->mech->success;
}

=head NAME

GDC::Docs::UpdateTerms - Screenscraping hack to update GDC dictionary

=head SYNOPSIS

=head AUTHOR

 Mark A. Jensen < mark -dot- jensen -at- nih -dot- gov >

=cut

1;
