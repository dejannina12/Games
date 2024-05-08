//for loops
// for (let i = 0; i < 5; i++) {
//   console.log("in loop: ", i);
// }

// console.log("loop finished");

// const names = ["shaun", "mario", "luigi"];

// for (let i = 0; i < names.length; i++) {
//   console.log(names[i]);
//   let html = `<div>${names[i]}</div>`;
//   console.log(html);
// }

//while loop
// let i = 0;
// while (i < 5) {
//   console.log("in loop ", i);
//   i++;
// }
// while (i < names.length) {
//   console.log(names[i]);
//   i++;
// }

//do while loops
// let i = 7;
// do {
//   console.log("value of i is: ", i);
//   i++;
// } while (i < 5);

//if statements
// const age = 25;
// if (age > 20) {
//   console.log("you are over 20");
// }
// const ninjas = ["shaun", "mario", "luigi", "dejan"];

// if (ninjas.length > 3) {
//   console.log("that's a lot of ninjas");
// }
// const password = "p@ss12";
// if (password >= 12 && password.includes("@")) {
//   console.log("that pass is mighty strong");
// } else if (
//   password.length >= 8 ||
//   (password.includes("@") && password.length >= 5)
// ) {
//   console.log("the password is long enough");
// } else {
//   console.log("password not long enough");
// }

//logical NOT (!)
// let user = false;
// if (!user) {
//   console.log("u must be lloged to continue");
// }
// console.log("true");
// console.log("false");

//break and continue

// const scores = [50, 25, 0, 30, 100, 20, 10];
// for (let i = 0; i < scores.length; i++) {
//   if (scores[i] === 0) {
//     continue;
//   }
//   console.log("your score: ", scores[i]);
//   if (scores[i] === 100) {
//     console.log("congrats, you got to the top");
//     break;
//   }
// }

//switch statements
// const grade = "D";
// switch (grade) {
//   case "A":
//     console.log("perfect");
//     break;
//   case "B":
//     console.log("very well");
//     break;
//   case "C":
//     console.log("good");
//     break;
//   case "D":
//     console.log("not good");
//     break;
//   case "E":
//     console.log("bad");
//     break;

//   default:
//     console.log("not valid grade");
//     break;
// }

//variables&block scope
let age = 30;
if (true) {
  let age = 40;
  console.log("inside: ", age);
}
console.log("outside: ", age);
