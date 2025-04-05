<!DOCTYPE html>
<html lang="en">
<head>
<title>This the Home page for Selenium testings</title>
<script>
    function showHiddenMessage() {
        document.getElementById("hiddenMessage").value = "You Clicked!";
        alert("You clicked!");
    }

</script>
</head>
<body>
    <?php
    echo("<p>This the home page</p><br>");
    echo("<input type='hidden' id='message' value='Hi'><br>");
    echo("<button type='button' id='inputClickMe' onclick='showHiddenMessage()'>Click Me!</button>");
    echo("<p id='hiddenMessage' value=''></p><br>")
    ?>
</body>
</html>

