function makeGrid(results) {
  var columnDefs = getColumnDefs(results.meta.fields);
  var gridOptions = {
    defaultColDef: {
      editable: true,
      sortable: true,
      filter: true
    },
    columnDefs: columnDefs,
    rowData: results.data,
    rowSelection: 'multiple',
    enableCellTextSelection: true,
    onGridReady: function(params) {
      params.api.sizeColumnsToFit();
      window.addEventListener('resize', function() {
        setTimeout(function() {
          params.api.sizeColumnsToFit();
        })
      })
    }
  };
  var eGridDiv = document.querySelector('#myGrid');
  new agGrid.Grid(eGridDiv, gridOptions);
}

function getColumnDefs(fields) {
  var columnDefs = [];
  for (var i = 0; i < fields.length; i++) {
    columnDefs.push({
      headerName: fields[i],
      field: fields[i]
    });
  }
  return columnDefs;
}
