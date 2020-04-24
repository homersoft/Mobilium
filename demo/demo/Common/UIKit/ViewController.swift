//
//  ViewController.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    init() {
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    // MARK: - View creation

    override func loadView() {
        let view = UIView()
        self.view = view
        view.backgroundColor = .systemBackground
        initializeSubviews()
        createConstraints()
    }

    // This function should be override to add subviews
    func initializeSubviews() {}

    // This function should be override to create constraints
    func createConstraints() {}
}
