<?php
    header('Content-type: text/html');
    session_start();
?>

<html>
    <head>  
        <title>Print the working directory.</title>

        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
 
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link href="https://fonts.googleapis.com/css?family=Raleway+Dots" rel="stylesheet">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <link rel="stylesheet" type="text/css" href="/static/css/base.css">

    </head>
    <body style="font-family: 'Lucida Sans Typewriter', 'Lucida Console', Monaco, 'Bitstream Vera Sans Mono', monospace;">

    <body style="font-family: 'Lucida Sans Typewriter', 'Lucida Console', Monaco, 'Bitstream Vera Sans Mono', monospace;">
 
      <div class="jumbotron">
        <div class="container text-center">
          <h1>
            Hacker Bar
            <img src="/static/images/TiltedM.png" style="width:6%;heigth:6%; ">
          </h1>
        </div>
      </div>
 
      <div class="navbar-more-overlay"></div>
        <nav class="navbar navbar-inverse navbar-fixed-top animate">
          <div class="container navbar-more visible-xs">
           <form class="navbar-form navbar-left" role="search">
             <div class="form-group">
               <div class="input-group">
                 <input type="text" class="form-control" placeholder="Search for...">
                 <span class="input-group-btn">
                   <button class="btn btn-default" type="submit">Submit</button>
                 </span>
               </div>
             </div>
           </form>
           <ul class="nav navbar-nav"></ul>
         </div>
         <div class="container">
           <div class="navbar-header hidden-xs">
             <a class="navbar-brand" href="#">Hacker Bar</a>
           </div>
 
           <ul class="nav navbar-nav navbar-right mobile-bar">
             <li>
               <a href="/cgi-bin/index.php">
                 <span class="menu-icon  glyphicon glyphicon-home"></span>
                 Home
               </a>
             </li>
             <li>
               <a href="/cgi-bin/menu.php">
                 <span class="menu-icon glyphicon glyphicon-glass"></span>
                  Menu
               </a>
             </li>
             <li>
               <a href="/cgi-bin/recent_orders.php">
                 <span class="menu-icon glyphicon glyphicon-shopping-cart"></span>
                 Orders
	       </a>
	     </li>
                <?php
                    if(!(!is_null($_SESSION['username']) && $_SESSION['username'] != '')){
            
                //{% if current_user.is_unauthenticated %}
                ?>  
	     <li>
               <a href="/cgi-bin/login.php">
                 <span class="menu-icon glyphicon glyphicon-home"></span>
                 Sign In
	      </a>
            </li>
           </ul>
         </div>
        </nav>
            <?php
		}else{
	    //else
            ?>
             <li>
               <a href="/cgi-bin/logout.php">
                 <span class="menu-icon glyphicon glyphicon-home"></span>
                 Sign Out
               </a>
             </li>
           </ul>
         </div>
        </nav>
            <?php
		}
	    //endif	
            ?>
