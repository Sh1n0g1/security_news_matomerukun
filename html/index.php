<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>セキュリティニュースまとめ君</title>
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <link href="data:image/x-icon;base64,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" rel="icon" type="image/x-icon" />
  
</head>
<body>
  <h3>セキュリティニュースまとめる君</h3>
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

