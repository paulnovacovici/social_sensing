    /*
    Filters table depending on search
    */
    function myFunction() {
      var input, filter, table, tr, td, i;
      input = document.getElementById("myInput");
      filter = input.value.toUpperCase();
      table = document.getElementById("myTable");
      tr = table.getElementsByTagName("tr");
      for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        td2 = tr[i].getElementsByTagName("td")[1];
        td3 = tr[i].getElementsByTagName("td")[2];
        if (td) {
          if (td.innerHTML.toUpperCase().indexOf(filter) > -1 
            || td2.innerHTML.toUpperCase().indexOf(filter) > -1 
            || td3.innerHTML.toUpperCase().indexOf(filter) > -1 ) {
            tr[i].style.display = "";
          } else {
            tr[i].style.display = "none";
          }
        }       
      }
    }

    var txtFile = new XMLHttpRequest();
    txtFile.open("GET", "http://localhost:8000/purchase_log.txt", true);

    /*
    Push to table from purchase log
    */
    txtFile.onreadystatechange = function()
    {
      if (txtFile.readyState === 4) {  // document is ready to parse.
        if (txtFile.status === 200) {  // file is found
          allText = txtFile.responseText; 
          lines = txtFile.responseText.split("\n");
          var table = document.getElementById("myTable");
          for (var line in lines){
            arr = lines[line].split("\t");
            var tr = document.createElement("tr");
            var td_date = document.createElement("td");
            var td_market = document.createElement("td");
            var td_ticker = document.createElement("td");
            var date = document.createTextNode(arr[0]);
            var market = document.createTextNode(arr[1]);
            var ticker = document.createTextNode(arr[2]);

            td_date.appendChild(date);
            td_market.appendChild(market);
            td_ticker.appendChild(ticker);
            tr.appendChild(td_date);
            tr.appendChild(td_market);
            tr.appendChild(td_ticker);
            table.appendChild(tr);
          }
        }
      }
    }
    txtFile.send(null);