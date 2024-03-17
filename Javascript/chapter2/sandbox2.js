//function declaration
// function greet() {
//   console.log("hello there");
// }
//greet();

//function expression
// const speak = function (name = "liigi", time = "nighy") {
//   console.log(`good ${time} ${name}`);
// };
// speak("mario");

// const calcArea = function (raduis) {
//   return 3.14 * raduis ** 2;
// };

// const calcVol = function (area) {};
// calcVol(area);
// const calcArea = (raduis) => {
//   return 3.14 * raduis ** 2;
// };
// const area = calcArea(5);
// console.log(area);

// const name = "shaun";
// //functions
// const greet = () => "hell";
// let resultOne = greet();
// console.log(resultOne);
// //methods
// let res = name.toUpperCase();
// console.log(res);

// const myFunc = (callbackFunc) => {
//   let value = 50;
//   callbackFunc(value);
// };
// myFunc(function (value) {
//   console.log(value);
// });

// const ul = document.querySelector(".people");
// const people = ["mario", "luigi", "shuan", "ruy", "shuj-li", "dejan"];
// // const logPerson = (person, index) => {
// //   console.log(`${index} - hello ${person}`);
// // };
// // people.forEach(logPerson);
// let html = ``;
// people.forEach((person) => {
//   html += `<li style="color: purple">${person}</li>`;
// });
// console.log(html);
// ul.innerHTML = html;

//object literals

// const blogs = [
//   { title: "why mac and chese", likes: 30 },
//   { title: "10 things to make", likes: 50 },
// ];
// console.log(blogs);
// let user = {
//   name: "crystal",
//   age: 30,
//   email: "crystal@thenetninja.co.uk",
//   location: "berlin",
//   blogs: [
//     { title: "why mac and chese", likes: 30 },
//     { title: "10 things to make", likes: 50 },
//   ],
//   login: function () {
//     console.log("user logged in");
//   },
//   logout() {
//     console.log("user logged out");
//   },
//   logBlogs() {
//     // console.log(this.blogs);
//     console.log("the user has written: ");
//     this.blogs.forEach((blog) => {
//       console.log(blog.title, blog.likes);
//     });
//   },
// };

// user.logBlogs();
// console.log(this);
// user.login();
// user.logout();
// console.log(user);
// console.log(user.name);
// //user.age = 35;
// console.log(user.age);
// console.log(user["age"]);
// const key = "location";
// console.log(user[key]);
// console.log(typeof user);

//Math objects
// console.log(Math);
// console.log(Math.PI);

// const area = 7.7;
// console.log(Math.round(area));
// //generate random numbers
// const random = Math.random();
// console.log(Math.round(random * 100));

//primitive values
let scoreOne = 50;
let scoreTwo = scoreOne;

console.log(`scoreone: ${scoreOne}`, `scoretwo: ${scoreTwo}`);
scoreOne = 100;
console.log(`scoreone: ${scoreOne}`, `scoretwo: ${scoreTwo}`);

//reference values
const userOne = { name: "ruy", age: 50 };
const userTwo = userOne;
console.log(userOne, userTwo);
userOne.age = 40;
console.log(userOne, userTwo);
