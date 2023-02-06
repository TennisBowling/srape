use futures::future::join_all;
use reqwest::{self, Client};
use axum::{
    routing::{get, post},
    http::StatusCode,
    response::IntoResponse,
    Json, Router,
};
use serde::{Deserialize, Serialize};
use serde_json;
use std::{net::SocketAddr, fs::File, io::Write, sync::Arc};
use tokio::time::{sleep, Duration};


#[tokio::main]
async fn main() {
    // build our application with a route
    let app = Router::new()
        .route("/", post(do_request)).layer(axum::extract::DefaultBodyLimit::max(100_000_000_000_000));

    // run our app with hyper
    // `axum::Server` is a re-export of `hyper::Server`
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn make_req(url: String, client: Arc<Client>) -> Option<String> {
    println!("making request to {}", url);
    if let Ok(res) = client.get(&url).send().await {
        println!("got response");
        return Some(res.text().await.unwrap());
    } else {
        println!("failed to get response");
        return None;
    }
}


#[derive(Deserialize)]
struct Requesturls {
    requesturls: Vec<String>,
}

async fn do_request(
    Json(body): Json<Requesturls>,
) -> impl IntoResponse {
    let mut futs = Vec::new();
    let client = Arc::new(reqwest::Client::new());
    println!("making {} requests", body.requesturls.len());
    for url in body.requesturls {
        futs.push(make_req(url, client.clone()));
        //sleep(Duration::from_millis(500)).await; // sleep for 500ms to avoid rate limiting (if you're not rate limited, you can remove this line
    }
    println!("made {} requests", futs.len());
    let responses = join_all(futs).await;
    let mut response: Vec<String> = Vec::new();
    println!("got {} responses", responses.len());
    for res in responses {
        if let Some(res) = res {
            response.push(res);
        }
    }
    println!("got {} responses", response.len());

    // write Json(response) to file
    //println!("Writing to file");
    //let mut file = File::create("essaysraw.json").unwrap();
    //file.write_all(serde_json::to_string(&response).unwrap().as_bytes()).unwrap();
    //println!("Wrote to file");

    (StatusCode::OK, Json(response))
}