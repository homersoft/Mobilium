//
//  PickerView.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Grzegorz Przybyła. All rights reserved.
//

import UIKit

class PickerView: UIPickerView {
    var onDone: (() -> Void)?
    let toolBar = UIToolbar()
        .set(\.barStyle, to: .default)
        .set(\.isTranslucent, to: true)
        .set(\.tintColor, to: UIColor(red: 76/255, green: 217/255, blue: 100/255, alpha: 1))

    override init(frame: CGRect) {
        super.init(frame: frame)
        initialize()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        initialize()
    }


    private func initialize() {
        toolBar.sizeToFit()
        let doneButton = UIBarButtonItem(title: "Done", style: .done, target: self, action: #selector(onDoneTouched))
        toolBar.setItems([doneButton], animated: true)
        toolBar.isUserInteractionEnabled = true
    }

    @objc private func onDoneTouched(_ sender: Any) {
        onDone?()
    }
}
