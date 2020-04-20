//
//  AvatarImageView.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Grzegorz Przybyła. All rights reserved.
//

import UIKit

class AvatarImageView: UIImageView, InputField {
    let chooseImageButton: UIButton = {
        let button = UIButton.makeForAutolayout()
        button.setTitle("Change", for: .normal)
        return button
    }()
    override init(frame: CGRect) {
        super.init(frame: frame)
        initialize()
    }

    func forceValidation() -> Bool {
        let isValid = image != nil
        layer.borderWidth = isValid ? 0.0 : 1.0
        return isValid
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        initialize()
    }

    private func initialize() {
        isUserInteractionEnabled = true
        layer.borderColor = UIColor.red.cgColor
        addSubview(chooseImageButton)
        NSLayoutConstraint.activate([
            chooseImageButton.bottomAnchor.constraint(equalTo: bottomAnchor),
            chooseImageButton.leadingAnchor.constraint(equalTo: leadingAnchor),
            chooseImageButton.trailingAnchor.constraint(equalTo: trailingAnchor)
        ])
    }
}
