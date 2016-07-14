#!/usr/bin/perl

# I declare that the attached assignment is wholly my own work in accordance with
# Seneca Academic Policy. No part of this assignment has been copied manually or
# electronically from any other source (including web sites) or distributed to other students.
# Name: Mandhir Bajaj
# ID: 103 230 157

use strict;
use warnings;
use DBI;
require '/home/bif724_161a03/.secret';
require 'mandhir_a1_lib.pl';

#   VIEW. This program generates a webpage that has the data from the table.

#headings for the columns for re1 id, score, and target gene id will be links
#clicking on the links will sort the coloumn according to that coloumn

print "Content-type: text/html\n\n";

# store db password in a var for easy access
my $password = get_passwd();
# This program adds a row of data to the db
# Works with table created with the command

# get a database handle, using the connection string for your system and use or die in case of errors
my $dbh = DBI-> connect("DBI:mysql:host=db-mysql;database=bif724_161a03", "bif724_161a03" ,$password) or die "Problem connecting" . DBI->errstr;

#formulate the insert query to be run
my $sql = "select * from a1_data";

#sql statement for ordering by certain column
#select * from a1_data order by re1_id ASC;

#use prepare function to prepare the query and get a statement handle and use or die in case of errors
my $sth = $dbh->prepare($sql) or die "problem with prepare" . DBI->errstr;
#execute the query and use or die in case of errors
my $success = $sth->execute() or die "problem with execute" . DBI->errstr;

print top_html("RE1 target gene data VIEW Page");

print <<T_TOP;
        <table border="1" cellspacing="0" width="50%">
                <tr><th><a href="http://zenit.senecac.on.ca/~bif724_161a03/mandhir_a1_view_sorted1.cgi">Re1_ID</th><th><a href="http://zenit.senecac.on.ca/~bif724_161a03/mandhir_a1_view_sorted2.cgi">Score</th><th><a href="http://zenit.senecac.on.ca/~bif724_161a03/mandhir_a1_view_sorted3.cgi">Target Gene id</th><th>Re1 Relative Position</th><th>Gene Strand</th><th>Description</th></tr>
T_TOP

if ($success != 0) {

        #loop through dataset if data found
        while (my @row = $sth->fetchrow_array) {
                my $ensembl_link = 'http://uswest.ensembl.org/Gene/Summary?db=core;g='.$row[2];
                print "<tr><td>$row[0]</td><td>$row[1]</td><td><a href='$ensembl_link' target='_blank'>$row[2]</td><td>$row[3]</td><td>$row[4]</td><td>$row[5]</td></tr>";

        }
        print "</table>";
        
        print '<br> GO to the <a href="http://zenit.senecac.on.ca/~bif724_161a03/mandhir_a1_add.cgi">ADD Page. ';
        
} else {
      # print a message if no data found
    print "<tr colspan='3'><td>no records found</td></tr>";
}

# release db connection and use or die in case of errors
$dbh->disconnect() or die "Problem disconnecting" . DBI->errstr;
print "</table>";
print bottom_html();