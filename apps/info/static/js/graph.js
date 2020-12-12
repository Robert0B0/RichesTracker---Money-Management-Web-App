var expense_dates = JSON.parse("{{expenses_dates|escapejs}}");
    var expense_values = JSON.parse("{{expenses_values|escapejs}}");

    buildExpensesChart()
    function buildExpensesChart(){
        var chartData = {
            "type":"bar",
            "scale-x":{
                "values": expense_dates
            },
            "series":[
                {
                    "values": expense_values 
                }
            ]
        }
        
        zingchart.render({
            id: "Expenses_Chart",
            data: chartData,
        });
    } 


    var income_dates = JSON.parse("{{income_dates|escapejs}}");
    var income_values = JSON.parse("{{income_values|escapejs}}");

    buildIncomeChart()
    function buildIncomeChart(){
        var chartData = {
            "type":"bar",
            "scale-x":{
                "values": income_dates
            },
            "series":[
                {
                    "values": income_values 
                }
            ]
        }
        
        zingchart.render({
            id: "Income_Chart",
            data: chartData,
        });
    } 




    var incomes = JSON.parse("{{all_income|escapejs}}");
    var outcomes = JSON.parse("{{all_outcome|escapejs}}");
    var dates = JSON.parse("{{all_dates|escapejs}}");

    buildOverViewChart()
    function buildOverViewChart() {
      let chartConfig = {
        type: 'bar',
        backgroundColor: '#FBFCFE',
        title: {
          text: 'Income and Outcome Chart',
          align: 'left',
          padding: '15px',
          fontColor: '#1E5D9E',
          fontFamily: 'Lato',
          fontSize: '16px'
        },
        subtitle: {
          text: 'Case Study',
          align: 'left',
          padding: '15px',
          fontColor: '#777',
          fontFamily: 'Lato',
          fontSize: '12px'
        },
        legend: {
          align: 'right',
          borderWidth: '0px',
          item: {
            fontColor: '#777'
          },
          layout: 'x2',
          marker: {
            borderRadius: '50px'
          }
        },
        plot: {
          tooltip: {
            visible: false
          },
          backgroundColor: '#FBFCFE',
          barSpace: '2px',
          marker: {
            size: 3.5
          }
        },
        plotarea: {
          margin: '90 50 50 50'
        },
        scaleX: {
          values: dates,
          margin: '20px',
          padding: '20px',
          guide: {
            lineColor: '#D7D8D9',
            lineGapSize: '4px',
            lineStyle: 'dotted',
            rules: [
              {
                rule: '%i == 0',
                visible: false
              }
            ],
            visible: true
          },
          item: {
            padding: '5px',
            fontColor: '#1E5D9E',
            fontFamily: 'Montserrat'
          },
          lineWidth: '0px',
          offsetY: '-20px',
          tick: {
            lineColor: '#D1D3D4'
          },
          transform: {
            type: 'date',
            all: '%d/%m/%y'
          }
        },
        scaleY: {
          guide: {
            lineColor: '#D7D8D9',
            lineGapSize: '4px',
            lineStyle: 'dotted',
            rules: [
              {
                rule: '%i == 0',
                visible: false
              }
            ],
            visible: true
          },
          item: {
            padding: '0 10 0 0',
            fontColor: '#1E5D9E',
            fontFamily: 'Montserrat'
          },
          lineWidth: '0px',

          tick: {
            lineColor: '#D1D3D4'
          }
        },
        crosshairX: {
          lineColor: '#b6b6b6',
          lineStyle: 'dashed',
          marker: {
            size: '4px',
            visible: true
          },
          plotLabel: {
            padding: '15px',
            backgroundColor: 'white',
            bold: true,
            borderColor: '#e3e3e3',
            borderRadius: '5px',
            fontColor: '#2f2f2f',
            fontFamily: 'Lato',
            fontSize: '12px',
            shadow: true,
            shadowAlpha: 0.2,
            shadowBlur: 5,
            shadowColor: '#a1a1a1',
            shadowDistance: 4,
            textAlign: 'right'
          },
          scaleLabel: {
            paddingTop: '2px',
            backgroundColor: '#FBFCFE',
            bold: true,
            callout: false,
            fontColor: '#1E5D9E',
            fontSize: '16px'
          },
          trigger: 'move'
        },
        source: {
          text: 'theatlas.com',
          fontColor: '#777',
          fontFamily: 'Lato'
        },
        series: [
          {
            text: 'Income',
            values: incomes,
            backgroundColor: '#1c9923'
          },
          {
            text: 'Outcome',
            values: outcomes,
            backgroundColor: '#921919'
          }
        ]
      };
      
      zingchart.render({
        id: 'OverViewChart',
        data: chartConfig,
        height: '100%',
        width: '100%',
      });
    }

    