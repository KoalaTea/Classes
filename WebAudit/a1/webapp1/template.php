#!/usr/bin/php

<?php
	header('Content-type: text/html');
?>

<html>
    <head>  
        <title>Print the working directory.</title>

        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
 
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.  css">
        <link href="https://fonts.googleapis.com/css?family=Raleway+Dots" rel="stylesheet">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/base.css') }}">

    </head>
    <body style="font-family: 'Lucida Sans Typewriter', 'Lucida Console', Monaco, 'Bitstream Vera Sans   Mono', monospace;">

    <body style="font-family: 'Lucida Sans Typewriter', 'Lucida Console', Monaco, 'Bitstream Vera Sans   Mono', monospace;">
 
      <div class="jumbotron">
        <div class="container text-center">
          <h1>
            Hacker Bar
            <img src="{{ url_for('static', filename='images/TiltedM.png') }}" style="width:6%;heigth:6%; ">
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
            //{% if current_user.is_authenticated %}
              <li>
               <a href="/">
                 <span class="menu-icon  glyphicon glyphicon-home"></span>
                 Home
               </a>
             </li>
             <li>
               <a href="/menu">
                 <span class="menu-icon glyphicon glyphicon-glass"></span>
                  Menu
               </a>
             </li>
             <li>
               <a href="/recent_orders">
                 <span class="menu-icon glyphicon glyphicon-shopping-cart"></span>
                 Orders
               </a>
             </li>
           </ul>
         </div>
       </nav>
       //{% else %}
             <li>
               <a href="/login">
                 <span class="menu-icon  glyphicon glyphicon-home"></span>
                 Sign In
               </a>
             </li>
           </ul>
         </div>
       </nav>
       //{% endif %}
        <p> 
        <?php $browser = getenv('HTTP_USER_AGENT'); echo "The users browser is $browser\n"; 
        $vars = get_defined_vars(); echo "The vars are $vars\n";
        echo '<pre>'; print_r($vars); echo '</pre>'; ?>
        </p>
    </body> 
</html>
