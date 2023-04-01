<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>セキュリティニュースまとめ君</title>
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
</head>
<body>
  <h3>セキュリティニュースまとめ君</h3>
  <div class="w3-container">
  <?php
    //Customizable parameter
    $ARTICLES_PER_PAGE=10;

    $ARTICLE_DIR='../articles/';
    if(isset($_GET['page'])){
      $page=$_GET['page'];
      if(!is_numeric($page) || intval($page) != $page || $page <= 0){
        $page=1;
      }
    }else{
      $page=1;
    }
    $article_files = array_reverse(array_diff(scandir($ARTICLE_DIR), array('..', '.')));
    $num_of_articles = count($article_files);
    $i=0;
    foreach($article_files as $file){
      $i++;
      if($i <= ($page -1) * $ARTICLES_PER_PAGE){
        continue;
      }
      $article_json=json_decode(file_get_contents($ARTICLE_DIR.$file),true);
      $datetime=$article_json['datetime'];
      $title=$article_json['title'];
      $category=$article_json['category'];
      $category_result=$article_json['category_result'];
      
      $url=$article_json['url'];
      $text_size=$article_json['text_size'];
      $results=$article_json['results'];
      $summary="";
      foreach($results as $r){
        if($r["result"]){
          if(array_key_exists("response", $r)){
            if(array_key_exists("choices", $r['response'])){
              if(array_key_exists("message",$r['response']['choices'][0])){
                if(array_key_exists("content",$r['response']['choices'][0]['message'])){
                  $summary.=$r['response']['choices'][0]['message']['content'];
                }
              }
            }
          }
        }else{
          $summary.='エラーが発生しました。<br>記事ファイル名:'.$file.'<br>';
          if(strstr($r['error'], "Error code 502") !== False){
            $summary.='<div class="w3-text-red">CloudFlare Error Code 502</div>';
          }else{
            $summary.='<div class="w3-text-red">'.$r['error']."</div>";
          }
        }
      }
      print('<div class="w3-card w3-padding">');
      print('<div class="w3-row">');
      print('  <div class="w3-col l8 w3-lime w3-padding"><a href="'.$url.'" target="_blank">'.$title.'</a></div>');
      print('  <div class="w3-col l1 w3-padding w3-light-green"><span title="'.$category_result.'">'.$category.'</span></div>');
      print('  <div class="w3-col l2 w3-padding w3-green">'.explode('.',$datetime)[0].'</div>');
      print('  <div class="w3-col l1 w3-padding w3-gray">'.$text_size.'文字</div>');
      print('</div>');
      print('<div class="w3-row">');
      //Just in case, ChatGPT returns answer without html tag.
      if(strstr($summary,"<td>")===False && strstr($summary,"<li>")===False){
        $summary=nl2br($summary);
      }
      print('  <div class="w3-col l12 summary">'.$summary.'</div>');
      print('</div>');
      print('</div><br>');
      if($i == $page * $ARTICLES_PER_PAGE){
        break;
      }
    }
  ?>
  </table>
  </div>
  <div class="w3-bar w3-center">
  <?php
    print('<a href="?page=1" class="w3-button">&laquo;</a>');
    for($i=1;$i < ($num_of_articles / $ARTICLES_PER_PAGE) + 1; $i++){
      if($i==$page){
        print('<span class="w3-button w3-green">'.$i.'</span>');
      }else{
        print('<a href="?page='.$i.'" class="w3-button">'.$i.'</a>');
      }
    }
    print('<a href="?page='.(floor($num_of_articles / $ARTICLES_PER_PAGE)+1).'" class="w3-button">&raquo;</a>');
    print('<span class="w3-small">(全'.$num_of_articles.'件)</span>');
  ?>
</div>
<footer class="w3-small w3-text-gray w3-right">本サイトはChatGPTにより記事の要約を作っています。<br>&copy;Sh1n0g1 All Right Reserved.</footer>
</body>
</html>

