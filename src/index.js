const { sendBountyAlert } = require('./services/notificationService');
const { formatBountyAlertTitle } = require('./utils/notificationFormatter');

module.exports = {
  sendBountyAlert,
  formatBountyAlertTitle
};
