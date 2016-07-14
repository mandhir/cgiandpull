#!/usr/bin/perl

# I declare that the attached assignment is wholly my own work in accordance with
# Seneca Academic Policy. No part of this assignment has been copied manually or
# electronically from any other source (including web sites) or distributed to other students.
# Name: Mandhir Bajaj
# ID: 103 230 157

use strict;
use warnings;
use CGI qw/:standard/;
require 'mandhir_a1_lib.pl';
require 'mandhir_a1_validation_lib.pl';
use DBI;
require '/home/bif724_161a03/.secret';
print "Content-type: text/html\n\n";
print top_html("RE1 target gene data ADD Page");

#   ADD. This program generates a form, processes the input form the user and adds it to the database.


# find out if we should process the form data or display the form
# if param is not empty then we should process the data.
if (param()) {
    # form must have been submitted, so validate data
    my $re1_id = param("re1");
    my $score = param("score");
    my $tgeneid = param("tgeneid");
    my $re1position = param("re1position");
    my $genedesc = param("genedesc");
    my $strand = param("strand");

    my @errors;
    # validate all fields
    
        my $pwd = get_passwd();
        
        ### Check for duplicates
        my $dbh = DBI-> connect("DBI:mysql:host=db-mysql;database=bif724_161a03", "bif724_161a03" ,$pwd) or die "Problem connecting" . DBI->errstr;

        my $sql = "select * from a1_data where re1_id=?";
        
        my $sth = $dbh->prepare($sql) or die "problem with prepare" . DBI->errstr;

        my $found = $sth->execute($re1_id);
    
        if ($found == 1) {
        push @errors, "The database already contains an entry where the Re1_ID is $re1_id";
        }
            
    if ($re1_id eq undef) {
        push @errors, "Re 1 ID cannot be NULL";
    } elsif (re1format($re1_id)!= 1) {
        push @errors, "Re 1 ID needs to be in the format 'organism_42_##*_#_########_f/r' \t eg. chicken_42_2_Z_320543_f or rat_42_34l_1_41581388_f or xenopus_42_41c_scaffold_509_538757_f";
    }
    
    if ($score eq undef)  {
        push @errors, "Re 1 ID cannot be NULL";
    } elsif (right_score($score) != 1) {
        push @errors, "Score can be a value between 0.91 and 1 with decimals of up to 4 decimal places";
    }
    
    if ($tgeneid eq undef) {
        push @errors, "Target Gene ID cannot be NULL";
    } elsif (tgenetest($tgeneid) != 1) {
        push @errors, "Target Gene ID needs to be in the format: ENSG00000117983 or ENSG###00000006297 with '3' representing letters";
    }
    
    if (tgeneid_species_match($re1_id,$tgeneid) != 1) {
        push @errors, "Species and Target Gene ID Do not match";
    }
    
    if ($re1position eq undef)  {
        push @errors, "Re 1 position cannot be NULL";
    } elsif (re1relpos($re1position) != 1) {
        push @errors, "RE 1 position can be one of (3', 5', exon, EXON, intron, INTRON, exon+, EXON+, intron+, INTRON+)";
    }

    if (desc_check($genedesc) != 1) {
        push @errors, "The gene description cannot have the following characters: / \\ \' \" ";
    }
    
    if (@errors) {
        # if there are validation errors, print the errors and form
        foreach (@errors) {
            print "$_<br>";
        }
        print "<br>";
        print "<br>";
        print "<br>";
        print myform();
    } else {
        
        my $pwd = get_passwd();
        
        ### IF DATA IS CORRECT
        my $dbh = DBI-> connect("DBI:mysql:host=db-mysql;database=bif724_161a03", "bif724_161a03" ,$pwd) or die "Problem connecting" . DBI->errstr;

        my $sql = "insert into a1_data values (?,?,?,?,?,?)";
        
        my $sth = $dbh->prepare($sql) or die "problem with prepare" . DBI->errstr;

        my $rows = $sth->execute($re1_id,$score,$tgeneid,$re1position,$strand,$genedesc);
        
        if ($rows == 1) {
        # print a success message if a row is inserted
        
        print "<br><br>Thank You for your data!";
        print "<META http-equiv='refresh' content='3;URL=mandhir_a1_view.cgi'>";
                
        } else {
          # print a message if no data found
        print "<p>couldnt insert data\n</p>";
        }
        
    }
} else {
    # form not submitted, so display form
    print myform();
}

print bottom_html();
sub myform {
    my $re1 = param('re1');
    my $score = param('score');
    my $tgeneid = param('tgeneid');
    my $re1position = param('re1position');
    my $strand = param('strand');
    my $positive = $strand eq '+'?"checked":"";
    my $negative = $strand eq '-'?"checked":"";
    my $genedesc = param('genedesc');
    return<<FORM;
    <form action="$0" method="get">
    <table border="0" width="40%">
        <tr><td width="25%">RE 1 ID:</td><td><input type="text" name="re1" value="$re1"></td></tr>
        <tr><td>Score:</td><td><input type="text" name="score" value="$score"></td></tr>
        <tr><td>Target Gene ID:</td><td><input type="text" name="tgeneid" value="$tgeneid"></td></tr>
        <tr><td>RE 1 Position:</td><td><input type="text" name="re1position" value="$re1position"></td></tr>
        <tr><td>Gene Description:</td><td><p><textarea cols='20' rows='6' name= "genedesc"></textarea><value="$genedesc"></td></tr>
        <tr><td></td></tr>
        <tr><td>Strand:</td>
            <td>
                Positive:<input type="radio" name="strand" value="+" $positive>
                Negative:<input type="radio" name="strand" value="-" $negative>
            </td></tr>
        <tr><td colspan="2" align="center"><input type="submit"></td></tr>
    </table>
    </form>
FORM

}