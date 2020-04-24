//
//  TextField.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import UIKit
class TextField: UITextField, InputField {
    var validator: Validator?
    private var observers: [NSObjectProtocol] = []
    private let underline = UIView.makeForAutolayout()
        .set(\.backgroundColor, to: .gray)

    override init(frame: CGRect) {
        super.init(frame: frame)
        initialize()
        initializeObservers()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        initialize()
        initializeObservers()
    }

    func forceValidation() -> Bool {
        validate()
    }

    deinit {
        observers = []
    }

    // MARK: - Private

    private func initialize() {
        addSubview(underline)
        NSLayoutConstraint.activate([
            underline.heightAnchor.constraint(equalToConstant: 1),
            underline.leadingAnchor.constraint(equalTo: leadingAnchor),
            underline.trailingAnchor.constraint(equalTo: trailingAnchor),
            underline.bottomAnchor.constraint(equalTo: bottomAnchor)
        ])
    }

    private func initializeObservers() {
        let notificationCenter = NotificationCenter.default
        observers.append(
            notificationCenter.addObserver(forName: UITextField.textDidEndEditingNotification,
                                           object: self, queue: .main) { [weak self] _ in
                                            self?.validate()
            }
        )
        observers.append(
            notificationCenter.addObserver(forName: UITextField.textDidChangeNotification,
                                           object: self, queue: .main) { [weak self] _ in
                                            self?.textColor = .black
                                            self?.underline.backgroundColor = .gray
            }
        )
    }

    @discardableResult
    func validate() -> Bool {
        guard let validator = validator else { return true }
        guard validator(text) else {
            textColor = .red
            underline.backgroundColor = .red
            return false
        }
        return true
    }
}
