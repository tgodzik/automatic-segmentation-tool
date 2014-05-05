import segmentation
if __name__ == "__main__":
    reference = ["./reference/segments3.json", "./reference/segments5.json"]
    pages = ["./pages/page3.html", "./pages/page5.html"]

    #segmentation.block_fusion_algorithm(pages, is_measured=False, visualized=True, treshold=0.4)

    # Block Fusion:
    #('./pages/page3.html', './reference/segments3.json') - [0.028093735106394783, 0.0]
    #('./pages/page5.html', './reference/segments5.json') - [0.009838305305234014, 0.0]

    segmentation.tree_segmentation_algorithm(pages, is_measured=False, measure_files=reference, visualized=True)

    # Tree matcher:
    #./pages/page3.html - [0.0, 0.0]
    #./pages/page5.html - [0.0, 0.0]
