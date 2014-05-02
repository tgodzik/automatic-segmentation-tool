from segmentation import block_fusion

if __name__ == "__main__":
    pages = [("./pages/page1.html", "./refrence/segments1.json")]
    block_fusion.algorithm(pages, is_measured=True, visualized=True, treshold=0.4)