sub top_html {
    my $title = shift;
    return<<TOP;
<!DOCTYPE html>
<html>
    <head>
        <title>$title</title>
    </head>
    <body>
TOP
}

sub bottom_html {
    return<<BOTTOM;
    </body>
</html>
BOTTOM
}


sub submit_form{
    return<<E;
    <form action="$0" method="post" enctype="multipart/form-data">
        file to upload: <input type="file" name="upfile"><br>
        <input type="submit">
    </form>
E
}

1;