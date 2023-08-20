const jsonfile = require('jsonfile');
const moment = require('moment');
const simpleGit = require('simple-git');
const { Random } = require('random-js');
const random = new Random();

const FILE_PATH = './data.json';

/**
 * Makes a commit with a randomly generated past date within the last year.
 * @param {number} n - Number of commits to make.
 */
const makeCommit = n => {
  if (n === 0) {
    return simpleGit().push(); // Push commits after completing all
  }

  // Generate random numbers for weeks and days
  const x = random.integer(0, 54); // Random integer between 0 and 54 weeks
  const y = random.integer(0, 6);  // Random integer between 0 and 6 days

  // Ensure the generated date does not exceed today's date
  const DATE = moment()
    .subtract(1, 'years')
    .add(1, 'days')
    .add(x, 'weeks')
    .add(y, 'days');

  // If the generated date is in the future, cap it to the current day
  const finalDate = DATE.isAfter(moment()) ? moment() : DATE;

  const formattedDate = finalDate.format();
  const data = { date: formattedDate };

  console.log(`Committing with date: ${formattedDate}`);  // ✅ Fixed line

  jsonfile.writeFile(FILE_PATH, data, () => {
    simpleGit()
      .add([FILE_PATH])
      .commit(formattedDate, { '--date': formattedDate }, makeCommit.bind(this, --n));
  });
};

makeCommit(56);
