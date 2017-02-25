#!/usr/bin/php-cgi

<?php include("templates/template.php") ?>

<link rel="stylesheet" type="text/css" href="/static/css/menu.css">
<script type="text/javascript" src="/static/js/menu.js"></script>

<div class="container" style="margin-top:5px">
  <div class="row">
    <div class="col">
      <div class="panel panel-default panel-table">
          <div class="panel-heading">
              <div class="tr">
                  <div class="td">
<?php
    if((!is_null($_SESSION['username']) && $_SESSION['username'] != '')){
        include("templates/menu_auth.php");
    }else{
        include("templates/menu_unauth.php");
    }
?>
          <div class="panel-footer">
              <div class="tr" align=center>
                  <div class="td">
                  <h5 class="drink-title">(END)</h5>
                  </div>
              </div>
          </div>
      </div>
    </div>
  </div>
</div>
<?php include("templates/templatebottom.php") ?>
