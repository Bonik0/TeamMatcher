const express = require('express');
const app = express();
const emailPage = require('./src/routers/emailPage')

app.set('views', __dirname + '/src/views');
app.set('view engine', 'ejs');

app.use('/email', emailPage)

app.listen(process.env.PORT);