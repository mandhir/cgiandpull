#!/usr/bin/perl -l

# I declare that the attached assignment is wholly my own work in accordance with
# Seneca Academic Policy. No part of this assignment has been copied manually or
# electronically from any other source (including web sites) or distributed to other students.
# Name: Mandhir Bajaj
# ID:103 230 157
use strict;
use warnings;
use CGI qw/:standard/;

use lib '/home/john.samuel/src/ensembl/modules';
use Bio::EnsEMBL::Registry;
use Bio::Graphics;
use Bio::SeqFeature::Generic;


print "Content-type: text/html\n\n";

#This program generates a form which asks for the following input:
#choose the chromosome
#start position text box
#end position text box
#submit button


my $informal_name = "Cow";

my $formal_name = "Bos taurus";

if (param()) {
    
    my $shuru = param('startpos');
    my $khatam = param('endpos');
    my $chr = param('chromosome');
    my @errors;
    
        if ($shuru>=$khatam) {
            push @errors, "<p>Your start position cannot be greater than or equal to your end position</p>";
        }
        if ($shuru !~ m/[0-9]/) {
            push @errors, "<p>Your start position can only have numbers (0-9)</p>";
        }
        if ($khatam !~ m/[0-9]/) {
            push @errors, "<p>Your start position can only have numbers (0-9)</p>";
        }
        if ((($khatam-$shuru)<1000) || (($khatam-$shuru)>10000000)) {
            push @errors, "<p>The difference between the start and end positions cannot be smaller than 1000 and greater than 10000,000</p>";
        }
    

                if (@errors) {
        
            print form_top("Submit Form");
            print "<p><font color='red'>@errors</font></p>";
            print form_body($informal_name, $formal_name);
            print form_end();

            } else {

            my $registry = 'Bio::EnsEMBL::Registry';
            $registry->load_registry_from_db(
            -host => 'ensembldb.ensembl.org',
            -user => 'anonymous'
            );
            
        #Success. So print table of genes and graphic.
            
        # this is the slice adaptor object

            my $slice_adaptor = $registry->get_adaptor( "$formal_name", 'Core', 'slice' );

        #now that I know start and end positions
        #we need a list of genes in the positions that the user selects

        ### this gives me a list of genes (& start&end positions) in selected region
        #
        ## get the slice to be shown in the image
            my $slice = $slice_adaptor->fetch_by_region('chromosome',"$chr",$shuru,$khatam);

            
            my $size = $khatam - $shuru;
            my $panel = Bio::Graphics::Panel->new(-length => $size, -width  => 800, -pad_left=>100, -pad_right=>100,
                -start=>$shuru,-end=>$khatam);

            # create an object to represent the scale bar
            my $scale = Bio::SeqFeature::Generic->new(-start => $shuru,-end => $khatam);
            # add the scale to the panel and adjust the settings 
            $panel->add_track($scale,-glyph => 'arrow',-tick => 2,-fgcolor => 'black',-double  => 1);
  
            print form_top("Retrieved Data from Ensembl");
    
            print results($informal_name, $formal_name, $chr, $shuru, $khatam);

            print "For the Chromosome you selected, Chromosome " . $slice->seq_region_name();

        ## this gives us start and end for the whole chromosome
            print "<br>The start position you selected is " . $slice->start();
            print "<br>The end position you selected is " . $slice->end();
            print "<br><br>";
            
            print <<START_TABLE;
        			<table border="1" cellspacing="0" width="50%">
                <tr><th>Gene_ID</th><th>Start</th><th>End</th><th>Strand</th><th>Length</th><th>Description</th><th>External Name</th><th>Gene Type</th><th>Status</th></tr>
START_TABLE

            if (@{$slice->get_all_Genes()}) {
                
            foreach my $gene (@{$slice->get_all_Genes()}) {
            	my $name = $gene->stable_id();
            	my $start = $gene->seq_region_start();
            	my $end = $gene->seq_region_end();
                my $strand = $gene->strand();
                my $desc = $gene->description();
                my $exname = $gene->external_name();
                my $gtype = $gene->biotype();
                my $status = $gene->status();
                
                my $length = $end - $start;
            
                my $colour = "";
                
                if ($gtype eq "protein_coding") {
                    $colour = "red";
                } else {
                    $colour = "black";
                }
                
                my $track = $panel->add_track(-glyph => 'transcript2', -stranded => 1,-label => 1, -fontcolor => "$colour", 
                            -bgcolor => 'green', -description=>"$desc");
                    
                # create an object to represent the gene
                my $feature = Bio::SeqFeature::Generic->new(-display_name => $name, -start => $start, -end => $end);
                # add the gene to the panel
                $track->add_feature($feature);
                
                my $link = "http://uswest.ensembl.org/Gene/Summary?db=core;g=".$name;
                
               print "<tr><td><a href=$link target=_blank>$name</td><td>$start</td><td>$end</td><td>$strand</td><td>$length</td><td>$desc</td><td>$exname</td><td>$gtype</td><td>$status</td></tr>";

            }

                print <<END_TABLE;
                        </table>
END_TABLE

            
            open FH, ">genelist.png" or die $!;
            print FH $panel->png;
            close FH;

                print "<br><br>";
                
                print "<img src='genelist.png'/>";

            
        } else {
                
                print "<tr><td>No Genes found</td></tr>";
                
            }

                   print <<END_TABLE;
                        </table>
END_TABLE
        
        print "<br><br>";
        
                print "<a href = 'http://zenit.senecac.on.ca/~bif724_161a03/a3/mandhir_a3.cgi'> Start Over";

                                
        }

    
    print form_end();
    
} else {

    #nothing submitted so print form

    my $start = param("startpos");
    my $end = param("endpos");


    print form_top("Submit Form");
    print "$start <br> $end <br>";
    print form_body($informal_name, $formal_name);
    
    print form_end();
    
}

#################
#The Subroutines#
#################

sub form_top {
    my $title = shift;
    return<<END;
<!DOCTYPE html>
<html>
<head>
<title>BIF 724 Assignment 3</title>
<strong>$title</strong><br><br>
</head>
END
}

sub form_body {
    my $name = shift;
    my $proper_name = shift;
    my $start = shift;
    my $end = shift;
    my $chr = shift;
    my $link = "http://useast.ensembl.org/index.html";
    my $html = "";
    $html .= <<END;
<body>
The organism that has been assigned is the $name <i>($proper_name)</i>.
<br><br>
Cows can be friendly but they don't smell very nice.
<br><br><br>

We will be extracting information from the <a href =$link>Ensembl Database</a>.
<br><br>

Example 1 (default):
<br><br><i>
Chromosome 1, Start Position: 1000000, End Position: 2000000.
<br><br></i>
Example 2:
<br><br><i>
Chromosome 8, Start Position: 500000, End Position: 1500000.
<br><br></i>
Example 3:
<br><br><i>
Chromosome 17, Start Position: 1, End Position: 500000.
</i>
<br><br>
    <form>
    <form action="$0" method="get">
    <br><br>
    Please select the chromosome you would like to look at below:
    <br><br>
    Chromosome: <select name = "chromosome"/>
END

	my @chr = (1..30);
	foreach (@chr) {
		my $selected = "";
		# for each item in list, see if it was previously set to this one
		$selected = " selected='selected'" if ($chr eq "$_");
		$html .= "<option $selected>$_</option>\n";
	}

    $html .= <<END;
			        </select>
    <br><br>
    And please specify the Chromosome Start and End Positions:
    <br><br>
      Chromosome Start Position:<br>
      <input type="text" name="startpos" value= "1000000">
      <br><br>
      Chromosome End Position:<br>
      <input type="text" name="endpos" value= "2000000">
      <br><br>
      <input type="submit">
    </form>
</body>
END

return $html;

}

sub form_end{
    return<<END
</html>
END
}

sub results {
    my $name = shift;
    my $fullname = shift;
    my $chromosomenumber = shift;
    my $start_position = shift;
    my $end_position = shift;
    
    return<<END
    <body>
    <br>
        Report for Region: $name <i>($fullname)</i> chromosome $chromosomenumber from position: $start_position to position: $end_position.
    <br><br>
    
END
}
