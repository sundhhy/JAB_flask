$(document).ready(function()
{
	// 页面加载时向pageLoad发送请求
	$.getScript("pageLoad")
})


// 周期性获取当前用户,当前页的相片
function onLoadHandler()
{
    // 向服务器发getPhoto GET请求
    $.getScript('getPhoto')

    setTimeout('onLoadHandler()', 2000)
    // $('#list').append("<div align='center'>test1</div>")
    // $('#list').append("<div align='center'> <a href='javascript:void(0)' onclick=\\\"showImg('test')\\\">test1</a></div>")
   
}

function uploadFile()
{
    var formData = new FormData($('form')[0])
    $.ajax({
        url: 'proUpload',
        type: 'POST',
        success:callback,
        err: function() {alert('文件上传服务器时出错，请联系管理员')},
        data: formData,
        //下面的选择用于告诉jQuery不要缓存数据且使用表单本身的contentType
        cache: false,
        contentType: false,
        processData: false
    })
}

function callback(msg)
{
    alert(msg)
    //隐藏文件上传对话框
    $('#uploadDiv').dialog('close')
    // 清空title, file两个表单域
    $('#title, #file').val('')
    $('#hideframe').attr('src', '')
}

function showImg(fileName)
{
    $.getScript('showImg?img='+fileName)
    
}

function openUpload()
{
    $("#uploadDiv").show()
        .dialog(
            {
                modal: true,
                title: '上传照片',
                resizeable: false,
                width: 428,
                height: 220,
                overlay: {opcity: 0.5, background: 'black'}
            }
        )

}

function turnPage(flag)
{
    $.getScript("turnPage?turn=" + flag)
}