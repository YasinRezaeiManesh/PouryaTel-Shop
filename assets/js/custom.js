function add_to_order(productId) {
    const productCount = $("#product_count").val();
    const productColor = $("#product_color").val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount + '&color=' + productColor).then(res => {
        Swal.fire({
            title: res.title,
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            confirmButtonText: res.confirm_button_text,
        }).then((result) => {
            if (result.isConfirmed && res.status === "user is not authenticated") {
                window.location.href = "/auth/login";
            }
        });
    });
}

function changeOrderDetailCount(detailId, state){
    $.get("/panel/change-order-detail-count?detail_id=" + detailId + "&state=" + state).then(res => {
        if (res.status === 'success') {
            $("#order-detail-content").html(res.body);
        }
    })
}

function removeOrderDetail(detailId){
    $.get('/panel/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            $("#order-detail-content").html(res.body);
        }
    })
}


function sendProductComment(product_Id) {
    var comment = $('#product_comment_text').val();
    var parentId = $('#product_parent_id').val();
    $.get('/products/product-comment/', {
        productComment: comment,
        productId: product_Id,
        parentId: parentId,
    }).then(res => {
        console.log(res);
        location.reload();
    });
}
