var mysql = require('mysql');

var db = mysql.createConnection({
  host : 'boaz-youplace.cai20ccufxe1.ap-northeast-2.rds.amazonaws.com',
  user : 'admin',
  password : 'youplace',
  database : 'db_youplace'
});

db.connect();

var sql = 'SELECT * FROM tb_youplace';

db.query(sql,(err,rows,fields) => {
  if (err){
    console.log(err);
  } else {
    console.log('rows',rows);
  }
});
conn.end();