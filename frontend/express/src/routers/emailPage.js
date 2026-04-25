const express = require('express')
const router = express.Router()



router.get('/verification', (req, res) => {
  const code = req.query.code || 'XXXXXX';
  res.render('emailVerification', { code });
});

module.exports = router