function upload_image() {
  initialize_results();
  $('.message').text('処理中...');

  var formData = new FormData($('#image_form').get(0));
  $.ajax({
    url: '/api/predict',
    type: 'post',
    processData: false,
    contentType: false,
    data: formData,
  }).done(function(results){
    $('.message').text('');
    if (results['err_message'] === undefined) {
      describe_results(results);
    } else {
      describe_error_message(results);
    }
  }).fail(function() {
    $('.message').text('');
    console.log('error!');
  });
  return false;
}

function describe_results(results) {
  describe_count_message(Object.keys(results['labels']).length);

  var table = $('.result_table');
  Object.keys(results['labels']).forEach(function(i) {
    var label = results['labels'][i];

    var row1 = $('<tr />');

    var faceId = $('<td />').append('(' + i + ')');
    faceId.attr('rowspan', 2);
    row1.append(faceId);

    row1.append($('<td />').append('年齢'));
    row1.append($('<td />').append(label['age']));
    table.append(row1);

    var row2 = $('<tr />');

    row2.append($('<td />').append('性別'));
    row2.append($('<td />').append(label['gender']));
    table.append(row2);
  });

  var image = $('<img />', {class: 'result_img'});
  image.attr('src', results['image']);
  $('#result_area').append(image);
}

function describe_error_message(results) {
  $('.message').text(results['err_message']);
}

function describe_count_message(num) {
  if (num === 0) {
    $('.message').text('お客様は入店していません。');
  } else {
    $('.message').text(num + '名のお客様が入店されました');
  }
}

function initialize_results() {
  $('.result_table').children('tr').remove();
  $('.result_img').remove();
}
