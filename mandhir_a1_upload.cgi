#!/usr/bin/perl

# I declare that the attached assignment is wholly my own work in accordance with
# Seneca Academic Policy. No part of this assignment has been copied manually or
# electronically from any other source (including web sites) or distributed to other students.
# Name: Mandhir Bajaj
# ID: 103 230 157

use strict;
use warnings;
use CGI qw/:standard/;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
require 'mandhir_a1_lib.pl';
use DBI;
require '/home/bif724_161a03/.secret';
require 'mandhir_a1_validation_lib.pl';
warningsToBrowser(1);
print "Content-type: text/html\n\n";
print top_html("RE1 target gene data UPLOAD Page");

#   UPLOAD. This program generates a upload form, uploads the file and adds it to the database.

if (param()) {
    # upload file
    # get file name

    my $upfilename = param('upfile');

    my @errors;
    
    if (checkfname($upfilename) == 1)
    {
    
    print "Thank you for uploading $upfilename<br>";
    # get filehandle
    my $upfh = upload('upfile');
    my @one_line = <$upfh>;    #<reads each line of file into element of array
#    open my $outfh, ">>", $upfilename or die "can't open $upfilename";

    my $pwd = get_passwd();
        
    my $dbh = DBI-> connect("DBI:mysql:host=db-mysql;database=bif724_161a03", "bif724_161a03" ,$pwd) or die "Problem connecting" . DBI->errstr;

    my $sql = "insert into a1_data values (?,?,?,?,?,?)";
        
        foreach (@one_line)
            {  #<-writes each element in array to a file
                my @allfieldsinline = (split (",", $_));
        
                if ((re1format($allfieldsinline[0]) == 1)
                    && (right_score($allfieldsinline[1]) == 1)
                    && (tgenetest($allfieldsinline[2]) == 1)
                    && (tgeneid_species_match($allfieldsinline[0],$allfieldsinline[2]) == 1)
                    && (re1relpos($allfieldsinline[3]) == 1)
                    && (strand_check($allfieldsinline[4]) == 1)
                    && (desc_check($allfieldsinline[5]) == 1))
                {
                my $sth = $dbh->prepare($sql) or die "problem with prepare" . DBI->errstr;
                my $rows = $sth->execute(@allfieldsinline);
                } else{
                 push @errors, $_; 
                }
                
            }
    
            #print errors if any, otherwise proceed
    
                if (@errors) {
                    foreach (@errors){
                        print $_;
                        print "<br>";
                    }
                    print submit_form();
                    } else {
                        print "<br><br>Thank You for your data!";
                        print "<META http-equiv='refresh' content='3;URL=mandhir_a1_view.cgi'>";            
                    }
        
    } else {
        print "The filename can only have letters, numbers, underscores and dashes.";
        print "<br>";
        print submit_form();
    }

} else {
    print submit_form();
}