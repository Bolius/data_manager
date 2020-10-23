const address_id = window.location.href.split("/").pop()

bbr_data = fetch_bbr_data('40eb1f85-9c53-4581-e044-0003ba298018')


document.addEventListener("DOMContentLoaded", function (event) {
  // bbr_data.then(res => insertBbrData(res["data"])).catch(err => {
  //   console.error(err);
  // });
});
