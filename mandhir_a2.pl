#!/usr/bin/perl -l
use strict;
use warnings;
use Bio::SeqIO;
use Bio::DB::GenBank;

#print "code disabled to avoid unnecessary use of ncbi\n";
#__END__
# get a genbank file by accession number

if (scalar(@ARGV)<2){
	print "You need to provide 2 command line arguments";
	print "First argument: name of the file containing the list of GenBank ids to be used";
	print "Second argument: name of the gene for which the sequences should be extracted"
	exit;
}	elsif (scalar(@ARGV)>2){
	print "What are you doing? Don't specify more than 2 arguments";
}

	#Create two Bio::SeqIO objects with the appropriate filenames
	my $db_o_dna = Bio::DB::GenBank->new;
	my $db_o_aa = Bio::DB::GenBank->new;

	my $accessionlist = $ARGV[0];
	my $wantedgene = $ARGV[1];

	open(line, $accessionlist) || die "Could not open file \n";
	while (my $accession = <line>) {

    my $dna_filename = "dna_mandhir".$wantedgene.".fa";
    my $aa_filename = "aa_mandhir".$wantedgene.".fa";

	my $seq_o = $db_o->get_Seq_by_acc($accession);

	if ($seq_o) {
	  # if a sequence object was retrieved, save a copy and process it
	  my $out = new Bio::SeqIO(-file=> ">>$dna_filename", -format=>'Fasta');
	  $out->write_seq($seq_o);

  		$out_aa = new Bio::SeqIO(-file=> ">>$aa_filename");
	  
	  #get and print info about sequence
	  print "The sequence is ", $seq_o->seq, "\n";
	  print "The accession number is ", $seq_o->accession_number, "\n";
	  print "The keywords are ", $seq_o->keywords, "\n";
	  print "The sequence length is ", $seq_o->length, "\n";
	  print "The description is ", $seq_o->desc, "\n";
	} else {
  	print "Unable to obtain sequence\n";
	}
}


  $out_dna = new Bio::SeqIO(-file=> ">>$dna_filename");
